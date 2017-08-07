# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Action(models.Model):
    """Model class that manage action."""

    _name = "qms.action"
    _description = "Action"

    _response_types_ = [
        ('immediate', 'Immediate Action'),
        ('correction', 'Corrective Action'),
        ('prevention', 'Preventive Action'),
        ('improvement', 'Improvement Opportunity')
    ]

    _complexity_levels_ = [
        ('very_low', 'Very Low'),
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('very_high', 'Very High')
    ]

    def _default_stage(self):
        """Return the default stage."""
        return self.env['qms.action.stage'].search(
            [('is_starting', '=', True)],
            limit=1
        )

    @api.model
    def _elapsed_days(self, dt1_text, dt2_text):
        res = 0
        if dt1_text and dt2_text:
            dt1 = fields.Datetime.from_string(dt1_text)
            dt2 = fields.Datetime.from_string(dt2_text)
            res = (dt2 - dt1).days
        return res

    @api.depends('opening_date',
                 'create_date')
    @api.one
    def _compute_days_to_open(self):
        for action in self:
            action.days_to_open = action._elapsed_days(
                action.create_date,
                action.opening_date
            )

    @api.depends('date_closed',
                 'create_date')
    @api.one
    def _compute_days_to_close(self):
        for action in self:
            action.days_to_close = action._elapsed_days(
                action.create_date,
                action.date_closed
            )

    name = fields.Char(
        string='Subject',
        required=True
    )

    active = fields.Boolean(
        default=True
    )

    date_deadline = fields.Date()

    create_date = fields.Datetime(
        readonly=True,
        default=fields.datetime.now()
    )

    cancel_date = fields.Datetime(
        readonly=True
    )

    opening_date = fields.Datetime(
        readonly=True
    )

    date_closed = fields.Datetime(
        readonly=True
    )

    days_to_open = fields.Integer(
        compute=_compute_days_to_open,
        store=True
    )

    days_to_close = fields.Integer(
        compute=_compute_days_to_close,
        store=True
    )

    description = fields.Html()

    type_action = fields.Selection(
        selection=_response_types_,
        string='Response Type',
        required=True
    )

    stage_id = fields.Many2one(
        comodel_name='qms.action.stage',
        copy=False,
        index=True,
        default=_default_stage,
        group_expand='_stage_groups'
    )

    reference = fields.Char(
        required=True,
        readonly=True,
        default='NEW'
    )

    complexity = fields.Selection(
        selection=_complexity_levels_,
        required=True
    )

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence']
        vals['reference'] = seq.next_by_code('qms.action')
        action = super(Action, self).create(vals)
        return action

    @api.multi
    def write(self, vals):
        if vals.get('stage_id'):
            if vals['stage_id'] == self._get_stage_new().id:
                if self.opening_date:
                    raise ValidationError(
                        _('We cannot bring back the action to draft stage')
                    )
                vals['cancel_date'] = None
            if vals['stage_id'] == self.env.ref('qms.stage_open').id:
                vals['opening_date'] = fields.Datetime.now()
                vals['date_closed'] = None
                vals['cancel_date'] = None
            if vals['stage_id'] == self.env.ref('qms.stage_close').id:
                if not self.opening_date or self.cancel_date:
                    raise ValidationError(
                        _('You should first open the action')
                    )
                vals['date_closed'] = fields.Datetime.now()
            if vals['stage_id'] == self.env.ref('qms.stage_cancel').id:
                vals['date_closed'] = None
                vals['opening_date'] = None
                vals['cancel_date'] = fields.Datetime.now()
        return super(Action, self).write(vals)

    @api.model
    def _stage_groups(self, stages, domain, order):
        stage_ids = self.env['qms.action.stage'].search([])
        return stage_ids

    @api.model
    def _get_stage_new(self):
        return self.env['qms.action.stage'].search(
            [('is_starting', '=', True)],
            limit=1
        )

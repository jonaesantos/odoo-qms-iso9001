# -*- coding: utf-8 -*-

from odoo import api, fields, models


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

    def _default_owner(self):
        """Return the user."""
        return self.env.user

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
    def _compute_number_of_days_to_open(self):
        for action in self:
            action.number_of_days_to_close_open = action._elapsed_days(
                action.create_date,
                action.opening_date
            )

    @api.depends('date_closed',
                 'create_date')
    def _compute_number_of_days_to_close(self):
        for action in self:
            action.number_of_days_to_close_open = action._elapsed_days(
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
        default=fields.Datetime.now()
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

    number_of_days_to_open = fields.Integer(
        '# of days to open',
        compute=_compute_number_of_days_to_open,
        store=True
    )

    number_of_days_to_close = fields.Integer(
        '# of days to close',
        compute=_compute_number_of_days_to_close,
        store=True
    )

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Responsible',
        default=_default_owner,
        required=True
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

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence']
        vals['reference'] = seq.next_by_code('qms.action')
        action = super(Action, self).create(vals)
        return action

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

    @api.model
    def _get_stage_open(self):
        return self.env.ref('qms_action.stage_open')

    @api.model
    def _get_stage_close(self):
        return self.env.ref('qms_action.stage_close')

    @api.model
    def _get_stage_cancel(self):
        return self.env.ref('qms_action.stage_cancel')

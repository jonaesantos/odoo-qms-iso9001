# -*- coding: utf-8 -*-
# This model is based in some code used in OCA Management System Addons Project
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Action(models.Model):

    _name = "qms.action"
    _description = "Action"

    _response_types_ = [
        ('immediate', 'Immediate Action'),
        ('correction', 'Corrective Action')
    ]

    _complexity_levels_ = [
        ('very_low', 'Very Low'),
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('very_high', 'Very High')
    ]    

    def _default_stage(self):
        return self.env['qms.action.stage'].search(
            [('is_starting', '=', True)],
            limit=1
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
        readonly=False
    )

    date_closed = fields.Datetime(
        readonly=False
    )

    description = fields.Html()

    response_type = fields.Selection(
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
        required=False,
        readonly=True
    )

    complexity = fields.Selection(
        selection=_complexity_levels_,
        required=True
    )

    responsible_id = fields.Many2one(
        comodel_name='qms.interested_party',
        required=True
    )

    effectiveness_check_ids = fields.One2many(
        comodel_name='qms.effectiveness_check',
        inverse_name='action_id',
        required=False
    )

    @api.model
    def create(self, vals):
        print
        print
        print "dentro de ............."
        print
        print
        print
        print
        print
        seq = self.env['ir.sequence']
        vals['reference'] = seq.next_by_code('qms.action')
        action = super(Action, self).create(vals)
        return action

    @api.multi
    def write(self, vals):
        print
        print
        print "dentro de <<<"
        print vals.get('stage_id')
        print
        print
        print
        print
        print
        # if vals.get('stage_id'):
        #     if vals['stage_id'] == self._get_stage_new().id:
        #         print
        #         print
        #         print "dentro de _get_stage_new()"
        #         print
        #         print
        #         print
        #         print
        #         print
            #     if self.opening_date:
            #         raise ValidationError(
            #             _('We cannot bring back the action to draft stage')
            #         )
            #     vals['cancel_date'] = None
            # if vals['stage_id'] == self.env.ref('qms.stage_open').id:
            #     print
            #     print
            #     print "dentro de open"
            #     print
            #     print
            #     print
            #     print
            #     print
            #     vals['opening_date'] = fields.Datetime.now()
            #     vals['date_closed'] = None
            #     vals['cancel_date'] = None
            # if vals['stage_id'] == self.env.ref('qms.stage_close').id:
            #     print
            #     print
            #     print "dentro de close"
            #     print
            #     print
            #     print
            #     print
            #     print
            #     if not self.opening_date or self.cancel_date:
            #         raise ValidationError(
            #             _('You should first open the action')
            #         )
            #     vals['date_closed'] = fields.Datetime.now()
            # if vals['stage_id'] == self.env.ref('qms.stage_cancel').id:
            #     vals['date_closed'] = None
            #     vals['opening_date'] = None
            #     vals['cancel_date'] = fields.Datetime.now()
        return super(Action, self).write(vals)

    @api.model
    def _stage_groups(self, stages, domain, order):
        print
        print
        print "dentro de _stage_groups"
        print
        print
        print
        print
        print
        stage_ids = self.env['qms.action.stage'].search([])
        return stage_ids

    @api.model
    def _get_stage_new(self):
        print
        print
        print "dentro de _get_stage_new 2"
        print
        #return self.env['qms.action.stage'].search(
        #    [('is_starting', '=', True)],
        #    limit=1
        return self.env['qms.action.stage'].search([])

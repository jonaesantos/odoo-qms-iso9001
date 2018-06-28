# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class Revision_by_direction(models.Model):

    _name = "qms.revision_by_direction"

    name = fields.Char(
        required=True
    )

    date_open = fields.Date()

    date_close = fields.Date()

    _states_ = [
        ('open', 'Open'),
        ('done', 'Closed')
    ]

    resource_ids = fields.Many2many(
        comodel_name='qms.resource'
    )

    action_ids = fields.Many2many(
        comodel_name='qms.action'
    )

    responsibles_ids = fields.Many2many(
        comodel_name='qms.interested_party',
        relation='audit_auditor_rel'
        #domain="[('auditor', '=', True)]"
    )

    opportunity_ids = fields.Many2many(
        comodel_name='qms.opportunity'
    )

    state = fields.Selection(
        selection=_states_,
        default='open'
    )

    @api.multi
    def button_close(self):
        return self.write(
            {
                'state': 'done',
                'closing_date': fields.Datetime.now()
            }
        )

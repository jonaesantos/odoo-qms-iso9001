# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Revision_by_direction(models.Model):

    _name = "qms.revision_by_direction"

    name = fields.Char(
        required=True
    )

    date_open = fields.Date()

    date_close = fields.Date()

    _state_ = [
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled')
    ]

    resource_ids = fields.Many2many(
        comodel_name='qms.resource'
    )

    action_ids = fields.Many2many(
        comodel_name='qms.action'
    )

    state = fields.Selection(
        selection=_state_,
        default='draft',
        required=True
    )

    responsibles_ids = fields.Many2many(
        comodel_name='qms.interested_party',
        relation='audit_auditor_rel'
        #domain="[('auditor', '=', True)]"
    )

    opportunity_ids = fields.Many2many(
        comodel_name='qms.opportunity'
    )

    @api.one
    def toggle_approved(self):
        self.approved = not self.approved

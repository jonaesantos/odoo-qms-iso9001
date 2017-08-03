# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Goal(models.Model):

    _name = "qms.goal"

    name = fields.Char()

    date = fields.Date()

    approved = fields.Boolean()

    policy_component_ids = fields.Many2many(
        comodel_name='qms.policy_component',
        required=True
    )

    process_ids = fields.Many2many(
        comodel_name='qms.process',
        required=True
    )

    resource_ids = fields.Many2many(
        comodel_name='qms.resource'
    )

    @api.one
    def toggle_approved(self):
        self.approved = not self.approved

# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Policy(models.Model):

    _name = "qms.policy"

    name = fields.Char(
        required=True
    )

    version = fields.Integer()

    date = fields.Date()

    approved = fields.Boolean()

    description = fields.Html()

    policy_component_ids = fields.Many2many(
        comodel_name='qms.policy_component',
        required=True
    )

    @api.one
    def toggle_approved(self):
        self.approved = not self.approved

# -*- coding: utf-8 -*-

from odoo import fields, models


class Policy(models.Model):

    _name = "qms.policy"

    name = fields.Char()

    revision = fields.Integer()

    date = fields.Date()

    approved = fields.Boolean()

    description = fields.Html()

    policy_component_ids = fields.Many2many(
        comodel_name='qms.policy_component',
        required=True
    )

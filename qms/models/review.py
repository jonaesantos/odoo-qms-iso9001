# -*- coding: utf-8 -*-

from odoo import fields, models


class Review(models.Model):

    _name = "qms.review"

    name = fields.Char(
        required=True
    )

    date = fields.Date()

    conclusion = fields.Html()

    policy_id = fields.Many2one(comodel_name='qms.policy')

    goal_id = fields.Many2one(comodel_name='qms.goal')

    process_id = fields.Many2one(comodel_name='qms.process')

    hazard_id = fields.Many2one(comodel_name='qms.hazard')

    interested_party_id = fields.Many2one(comodel_name='qms.interested_party')

    responsible_id = fields.Many2one(
        comodel_name='qms.interested_party',
        required=False
    )

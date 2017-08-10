# -*- coding: utf-8 -*-

from odoo import fields, models


class Effectiveness_Check(models.Model):

    _name = "qms.effectiveness_check"

    _states_ = [
        ('pending', 'Pending'),
        ('closed', 'Closed')
    ]

    expected_date = fields.Date()

    verification_date = fields.Date()

    was_effective = fields.Boolean()

    action_id = fields.Many2one(
        comodel_name='qms.action',
        required=True
    )

    state = fields.Selection(
        selection=_states_,
        default='pending'
    )

    observations = fields.Text()

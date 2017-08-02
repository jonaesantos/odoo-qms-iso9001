# -*- coding: utf-8 -*-

from odoo import fields, models


class Action_Stage(models.Model):
    """This object is used to defined different stage for actions."""

    _name = 'qms.action.stage'
    _description = "Action Stages"
    _order = 'sequence'

    name = fields.Char(
        required=True
    )

    sequence = fields.Integer(
        help="Used to order stages. Lower is better.",
        default=10
    )

    is_starting = fields.Boolean(
        string='Starting stage'
    )

    is_ending = fields.Boolean(
        string='Ending stage'
    )

# -*- coding: utf-8 -*-

from odoo import fields, models


class Stage(models.Model):

    _name = 'qms.stage'
    _order = 'sequence'

    name = fields.Char(
        required=True
    )

    sequence = fields.Integer(
        help="Used to order stages. Lower is better.",
        default=100
    )

    is_starting = fields.Boolean(
        string='Starting stage'
    )

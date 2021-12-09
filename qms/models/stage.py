from odoo import fields, models


class Stage(models.Model):

    _name = "qms.stage"
    _description = "Stage"
    _order = "sequence"

    name = fields.Char(required=True, translate=True)

    sequence = fields.Integer(
        help="Used to order stages. Lower is better.", default=100
    )

    is_starting = fields.Boolean(string="Starting Stage")

from odoo import fields, models


class Weakness(models.Model):

    _name = "qms.weakness"
    _description = "Weakness"

    analysis = fields.Text()

    cause_ids = fields.Many2many(comodel_name="qms.weakness.cause")

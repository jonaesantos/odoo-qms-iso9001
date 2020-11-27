
from odoo import fields, models


class Policy_Component(models.Model):

    _name = "qms.policy_component"

    name = fields.Char(
        required=True
    )

from odoo import fields, models


class PolicyComponent(models.Model):

    _name = "qms.policy_component"
    _description = "Policy Component"

    name = fields.Char(required=True)

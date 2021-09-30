from odoo import fields, models


class PolicyComponent(models.Model):

    _name = "qms.policy_component"

    name = fields.Char(required=True)

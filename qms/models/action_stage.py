from odoo import fields, models


class ActionStage(models.Model):

    _name = "qms.action.stage"
    _description = "Action Stage"
    _inherit = ["qms.stage"]

    is_ending = fields.Boolean(string="Ending Stage")

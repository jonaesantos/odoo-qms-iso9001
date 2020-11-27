
from odoo import fields, models


class Action_Stage(models.Model):

    _name = 'qms.action.stage'
    _inherit = ['qms.stage']

    is_ending = fields.Boolean(
        string='Ending stage'
    )

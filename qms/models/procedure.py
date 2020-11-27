
from odoo import api, fields, models, _


class Procedure(models.Model):

    _name = "qms.procedure"
    _inherit = 'qms.document'

    name = fields.Char(
        required=True
    )

    version_ids = fields.One2many(
        comodel_name='qms.version',
        inverse_name='procedure_id'
    )   
     
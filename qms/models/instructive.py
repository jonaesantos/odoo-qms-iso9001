
from odoo import api, fields, models, _


class Instructive(models.Model):

    _name = "qms.instructive"
    _inherit = 'qms.document'

    name = fields.Char(
        required=True
    )

    version_ids = fields.One2many(
        comodel_name='qms.version',
        inverse_name='instructive_id'
    )     
    
     
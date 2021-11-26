from odoo import fields, models


class Procedure(models.Model):

    _name = "qms.procedure"
    _description = "Procedure"
    _inherit = "qms.document"

    name = fields.Char(required=True)

    version_ids = fields.One2many(
        comodel_name="qms.version", inverse_name="procedure_id"
    )

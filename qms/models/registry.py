from odoo import fields, models


class Registry(models.Model):

    _name = "qms.registry"
    _description = "Registry"

    _inherit = "qms.document"

    name = fields.Char(required=True)

    version_ids = fields.One2many(
        comodel_name="qms.version", inverse_name="registry_id"
    )

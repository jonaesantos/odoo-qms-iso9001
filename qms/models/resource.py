from odoo import fields, models


class Resource(models.Model):

    _name = "qms.resource"
    _description = "Resource"

    responsible_id = fields.Many2one(
        comodel_name="qms.interested_party", required=True, ondelete="restrict"
    )

    name = fields.Char(required=True)

    description = fields.Html()

    resource_type = fields.Selection(
        selection=[
            ("internal", "Internal"),
            ("external", "External"),
        ]
    )

    state = fields.Selection(
        selection=[
            ("available", "Available"),
            ("in_process", "In Process"),
            ("not_available", "Not Available"),
        ],
        default="available",
    )

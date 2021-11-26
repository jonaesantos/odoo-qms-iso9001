from odoo import _, fields, models


class Resource(models.Model):

    _name = "qms.resource"
    _description = "Resource"

    _resource_types_ = [("internal", "Internal"), ("external", _("External"))]

    _resource_states_ = [
        ("available", _("Available")),
        ("in_process", _("In Process")),
        ("not_available", _("Not Available")),
    ]

    responsible_id = fields.Many2one(
        comodel_name="qms.interested_party", required=True
    )

    name = fields.Char(required=True)

    description = fields.Html()

    resource_type = fields.Selection(selection=_resource_types_)

    state = fields.Selection(selection=_resource_states_, default="available")

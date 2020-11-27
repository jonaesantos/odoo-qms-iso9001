
from odoo import fields, models


class Resource(models.Model):

    _name = "qms.resource"

    _resource_types_ = [
        ('internal', 'Internal'),
        ('external', 'External')
    ]

    _resource_states_ = [
        ('available', 'Available'),
        ('in_process', 'In Process'),
        ('not_available', 'Not Available')
    ]

    responsible_id = fields.Many2one(
        comodel_name='qms.interested_party',
        required=True
    )

    name = fields.Char(
        required=True
    )

    description = fields.Html()

    resource_type = fields.Selection(
        selection=_resource_types_
    )

    state = fields.Selection(
        selection=_resource_states_,
        default='available'
    )

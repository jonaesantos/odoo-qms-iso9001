# -*- coding: utf-8 -*-

from odoo import fields, models


class Interested_Party(models.Model):

    _name = "qms.interested_party"

    _interested_party_types_ = [
        ('internal', 'Internal'),
        ('external', 'External')
    ]

    name = fields.Char(
        required=True
    )

    interested_party_type = fields.Selection(
        selection=_interested_party_types_
    )

    is_organization = fields.Boolean()

    organization_id = fields.Many2one(
        comodel_name='qms.interested_party',
        domain=[('is_organization', '=', True)]
    )

    area = fields.Char()

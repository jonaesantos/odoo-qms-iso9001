# -*- coding: utf-8 -*-

from odoo import fields, models


class Interested_Party(models.Model):

    _name = "qms.interested_party"

    _interested_party_types_ = [
        ('internal', 'Internal'),
        ('external', 'External')
    ]

    _power_ = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
        (4, 'Very High')
    ]

    _interest_ = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
        (4, 'Very High')
    ]

    _cooperation_ = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
        (4, 'Very High')
    ]

    _impact_ = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
        (4, 'Very High')
    ]

    power = fields.Selection(
        selection=_power_,
        required=False
    )

    interest = fields.Selection(
        selection=_interest_,
        required=False
    )

    cooperation = fields.Selection(
        selection=_cooperation_,
        required=False
    )

    impact = fields.Selection(
        selection=_impact_,
        required=False
    )

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

    requeriments_interested_party = fields.Html()

    interest_tmc = fields.Html()

    area = fields.Char()

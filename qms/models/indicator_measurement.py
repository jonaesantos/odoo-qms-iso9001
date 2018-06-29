# -*- coding: utf-8 -*-
# This model is based in some code used in OCA Management System Addons Project
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, _


class Indicator_Measurement(models.Model):

    _name = "qms.indicator.measurement"

    name = fields.Char(
        string='Measurement',
        required=True
    )

    goal = fields.Char()

    indicator_id = fields.Many2one(
        comodel_name='qms.indicator',
        ondelete='cascade',
    )

    expected_date = fields.Date()

    measurement_date = fields.Date()

    comments = fields.Text()

    _result_ = [
        (1, 'Meta alcanzada'),
        (2, 'Meta alcanzada con observaciones'),
        (3, 'Meta no alzanzada')
    ]

    result = fields.Selection(
        selection=_result_,
        string='Result',
        required=False
    )

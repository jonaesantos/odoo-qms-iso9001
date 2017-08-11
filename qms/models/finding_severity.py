# -*- coding: utf-8 -*-
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class Finding_Severity(models.Model):

    _name = "qms.finding.severity"

    name = fields.Char(
        required=True,
        translate=True
    )

    sequence = fields.Integer()

    description = fields.Text()

    active = fields.Boolean(
        default=True
    )

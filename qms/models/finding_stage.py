# -*- coding: utf-8 -*-
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, _


class Finding_Stage(models.Model):

    _name = 'qms.finding.stage'
    _inherit = ['qms.stage']

    _states_ = [
        ('draft', _('Draft')),
        ('analysis', _('Analysis')),
        ('pending', _('Action Plan')),
        ('open', _('In Progress')),
        ('done', _('Closed')),
        ('cancel', _('Cancelled'))
    ]

    state = fields.Selection(
        selection=_states_,
        readonly=True,
        default='draft'
    )

    fold = fields.Boolean()

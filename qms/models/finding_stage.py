# -*- coding: utf-8 -*-

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

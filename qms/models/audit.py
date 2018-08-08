# -*- coding: utf-8 -*-
# This model is based in some code used in OCA Management System Addons Project
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _

class Audit(models.Model):

    _name = 'qms.audit'
    _rec_name = 'reference'

    _system_ = [
        ('iso9001_2015', 'ISO 9001:2015'),
        ('iso9001_2008', 'ISO 9001:2008')
    ]

    system = fields.Selection(
        selection=_system_,
        string='System',
        required=True
    )

    _states_ = [
        ('open', 'Open'),
        ('done', 'Closed')
    ]

    reference = fields.Char(
        readonly=False,
        required=False
    )

    date = fields.Datetime()

    verification_line_ids = fields.One2many(
        comodel_name='qms.audit.verification.line',
        inverse_name='audit_id',
    )

    closing_date = fields.Datetime(
        readonly=True
    )

    strong_points = fields.Html('Strong Points')

    state = fields.Selection(
        selection=_states_,
        default='open'
    )

    audited_ids = fields.Many2many(
        comodel_name='qms.interested_party',
        relation='audit_audited_rel'
        #domain="[('auditor', '=', False)]"
    )

    auditors_ids = fields.Many2many(
        comodel_name='qms.interested_party',
        relation='audit_auditor_rel'
        #domain="[('auditor', '=', True)]"
    )

    non_conformity_ids = fields.One2many(
        comodel_name='qms.non_conformity',
        inverse_name='audit_id'
    )

    observation_ids = fields.One2many(
        comodel_name='qms.observation',
        inverse_name='audit_id'
    )

    opportunity_ids = fields.One2many(
        comodel_name='qms.opportunity',
        inverse_name='audit_id'
    )

    process_ids = fields.Many2many(
        comodel_name='qms.process',
        required=True
    )

    # @api.model
    # def create(self, vals):
    #     vals.update({
    #         'reference': self.env['ir.sequence'].next_by_code(
    #             'qms.audit'
    #         ),
    #     })
    #     audit_id = super(Audit, self).create(vals)
    #     return audit_id

    @api.multi
    def button_close(self):
        return self.write(
            {
                'state': 'done',
                'closing_date': fields.Datetime.now()
            }
        )

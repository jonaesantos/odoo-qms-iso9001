# -*- coding: utf-8 -*-
# This model is based in some code used in OCA Management System Addons Project
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Audit(models.Model):

    _name = 'qms.audit'
    _rec_name = 'reference'

    _states_ = [
        ('open', 'Open'),
        ('done', 'Closed')
    ]

    reference = fields.Char(
        readonly=True,
        required=True
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

    to_improve_points = fields.Html('Points To Improve')

    state = fields.Selection(
        selection=_states_,
        default='open'
    )

    @api.model
    def create(self, vals):
        vals.update({
            'reference': self.env['ir.sequence'].next_by_code(
                'qms.audit'
            ),
        })
        audit_id = super(Audit, self).create(vals)
        return audit_id

    @api.multi
    def button_close(self):
        return self.write(
            {
                'state': 'done',
                'closing_date': fields.Datetime.now()
            }
        )

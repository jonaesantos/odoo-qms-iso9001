# -*- coding: utf-8 -*-

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
        default='NEW',
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

    # user_id = fields.Many2one('res.users', 'Audit Manager')

    # auditor_user_ids = fields.Many2many(
    #     'res.users',
    #     'qms_auditor_user_rel',
    #     'user_id',
    #     'qms_audit_id',
    #     'Auditors',
    # )
    #
    # auditee_user_ids = fields.Many2many(
    #     'res.users',
    #     'qms_auditee_user_rel',
    #     'user_id',
    #     'qms_audit_id',
    #     'Auditees',
    # )

    strong_points = fields.Html('Strong Points')

    to_improve_points = fields.Html('Points To Improve')

    # imp_opp_ids = fields.Many2many(
    #     'qms.action',
    #     'qms_audit_imp_opp_rel',
    #     'qms_action_id',
    #     'qms_audit_id',
    #     'Improvement Opportunities',
    # )

    # nonconformity_ids = fields.Many2many(
    #     'qms.nonconformity',
    #     string='Nonconformities',
    # )

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

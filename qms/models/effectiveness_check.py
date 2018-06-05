# -*- coding: utf-8 -*-

from odoo import _, fields, models, api

class Effectiveness_Check(models.Model):

    _name = "qms.effectiveness_check"

    _states_ = [
        ('pending', 'Pending'),
        ('closed', 'Closed')
    ]

    expected_date = fields.Date()

    verification_date = fields.Date()

    was_effective = fields.Boolean()

    action_id = fields.Many2one(
        comodel_name='qms.action',
        required=True
    )

    state = fields.Selection(
        selection=_states_,
        default='pending'
    )

    observations = fields.Text()

    @api.constrains('state')
    def _check_closed_with_verification_date(self):
        for effectiveness_check in self:
            if effectiveness_check.state == 'closed' and not effectiveness_check.verification_date:
                raise models.ValidationError(
                    _("verification_date are required \
                      in order to put a effectiveness_check 'closed'.")
                )

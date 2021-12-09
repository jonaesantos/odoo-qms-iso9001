# This model is based in some code used in OCA Management System Addons Project
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AuditVerificationLine(models.Model):

    _name = "qms.audit.verification.line"
    _description = "Audit Verification Line"

    _order = "seq"

    name = fields.Char(string="Question", required=True)

    clause = fields.Char(required=True)

    audit_id = fields.Many2one(
        comodel_name="qms.audit", ondelete="cascade", index=True
    )

    is_conformed = fields.Boolean()

    comments = fields.Text()

    seq = fields.Integer(string="Sequence")

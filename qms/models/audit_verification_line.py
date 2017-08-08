# -*- coding: utf-8 -*-

from odoo import fields, models


class Audit_Verification_Line(models.Model):

    _name = "qms.audit.verification.line"
    _order = "seq"

    name = fields.Char(
        string='Question',
        required=True
    )

    audit_id = fields.Many2one(
        comodel_name='qms.audit',
        ondelete='cascade',
        index=True
    )

    # procedure_id = fields.Many2one(
    #     'document.page',
    #     'Procedure',
    #     ondelete='restrict',
    #     index=True,
    # )

    is_conformed = fields.Boolean()

    comments = fields.Text()

    seq = fields.Integer(
        string='Sequence'
    )

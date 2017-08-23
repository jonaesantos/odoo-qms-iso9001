# -*- coding: utf-8 -*-
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models


class Weakness_Cause(models.Model):

    _name = "qms.weakness.cause"
    _order = 'parent_id, sequence'
    _parent_store = True
    _inherit = ['qms.finding.milestone']

    parent_id = fields.Many2one(
        comodel_name='qms.weakness.cause',
        string='Group',
        ondelete='restrict'
    )

    child_ids = fields.One2many(
        comodel_name='qms.weakness.cause',
        inverse_name='parent_id',
        string='Child causes'
    )

    @api.constrains("parent_id")
    def _check_recursion(self):
        if not super(Weakness_Cause, self)._check_recursion():
            raise exceptions.ValidationError(
                _("Error! Cannot create recursive cycle.")
            )

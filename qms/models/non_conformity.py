# -*- coding: utf-8 -*-
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, models


class Non_Conformity(models.Model):

    _name = "qms.non_conformity"
    _inherit = ['qms.finding']

    @api.model
    def create(self, vals):
        vals.update({
            'reference': self.env['ir.sequence'].next_by_code(
                'qms.non_conformity')
        })
        return super(Non_Conformity, self).create(vals)

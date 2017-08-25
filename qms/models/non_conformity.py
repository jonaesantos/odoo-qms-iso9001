# -*- coding: utf-8 -*-

from odoo import api, models


class Non_Conformity(models.Model):

    _name = "qms.non_conformity"
    _inherit = ['qms.finding', 'qms.weakness']

    @api.model
    def create(self, vals):
        vals.update({
            'reference': self.env['ir.sequence'].next_by_code(
                'qms.non_conformity')
        })
        return super(Non_Conformity, self).create(vals)

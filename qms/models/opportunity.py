# -*- coding: utf-8 -*-

from odoo import api, models


class Opportunity(models.Model):

    _name = "qms.opportunity"
    _inherit = ['qms.finding']

    @api.model
    def create(self, vals):
        vals.update({
            'reference': self.env['ir.sequence'].next_by_code(
                'qms.opportunity')
        })
        return super(Opportunity, self).create(vals)

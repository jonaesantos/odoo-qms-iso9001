# -*- coding: utf-8 -*-


from odoo import api, models


class Improvement(models.Model):

    _name = "qms.improvement"
    _inherit = ['qms.finding']

    @api.model
    def create(self, vals):
        vals.update({
            'reference': self.env['ir.sequence'].next_by_code(
                'qms.improvement')
        })
        return super(Improvement, self).create(vals)

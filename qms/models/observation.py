# -*- coding: utf-8 -*-

from odoo import api, models


class Observation(models.Model):

    _name = "qms.observation"
    _inherit = ['qms.finding', 'qms.weakness']

    @api.model
    def create(self, vals):
        vals.update({
            'reference': self.env['ir.sequence'].next_by_code(
                'qms.observation')
        })
        return super(Observation, self).create(vals)

# -*- coding: utf-8 -*-

from odoo import api, models


class Complaint(models.Model):

    _name = "qms.complaint"
    _inherit = ['qms.finding', 'qms.weakness']

    @api.model
    def create(self, vals):
        vals.update({
            'reference': self.env['ir.sequence'].next_by_code(
                'qms.complaint')
        })
        return super(Complaint, self).create(vals)

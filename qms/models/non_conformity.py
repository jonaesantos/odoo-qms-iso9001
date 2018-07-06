# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class Non_Conformity(models.Model):

    _name = "qms.non_conformity"
    _inherit = ['qms.finding', 'qms.weakness']

    action_ids = fields.One2many(
        comodel_name='qms.action',
        inverse_name='non_conformity_id'
    )

    @api.model
    def create(self, vals):
        vals.update({
            'reference': self.env['ir.sequence'].next_by_code(
                'qms.non_conformity')
        })
        return super(Non_Conformity, self).create(vals)

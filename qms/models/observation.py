# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class Observation(models.Model):

    _name = "qms.observation"
    _inherit = ['qms.finding', 'qms.weakness']

    action_ids = fields.One2many(
        comodel_name='qms.action',
        inverse_name='observation_id'
    )

    @api.model
    def create(self, vals):
        vals.update({
            'reference': self.env['ir.sequence'].next_by_code(
                'qms.observation')
        })
        return super(Observation, self).create(vals)

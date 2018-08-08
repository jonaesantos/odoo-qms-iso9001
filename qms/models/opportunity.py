# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class Opportunity(models.Model):

    _name = "qms.opportunity"
    _inherit = ['qms.finding']

    action_ids = fields.One2many(
        comodel_name='qms.action',
        inverse_name='opportunity_id'
    )

    audit_id = fields.Many2one(
        comodel_name='audit'
    )

    revision_by_direction_id = fields.Many2one(
        comodel_name='revision_by_direction'
    )            

    @api.model
    def create(self, vals):
        vals.update({
            'reference': self.env['ir.sequence'].next_by_code(
                'qms.opportunity')
        })
        return super(Opportunity, self).create(vals)

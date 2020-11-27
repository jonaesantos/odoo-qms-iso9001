
from odoo import api, fields, models, _


class Observation(models.Model):

    _name = "qms.observation"
    _inherit = ['qms.finding', 'qms.weakness']

    action_ids = fields.One2many(
        comodel_name='qms.action',
        inverse_name='observation_id'
    )

    audit_id = fields.Many2one(
        comodel_name='audit'
    )

    revision_by_direction_id = fields.Many2one(
        comodel_name='revision_by_direction'
    )

    indicator_id = fields.Many2one(
        comodel_name='indicator'
    )     

    @api.model
    def create(self, vals):
        vals.update({
            'reference': self.env['ir.sequence'].next_by_code(
                'qms.observation')
        })
        return super(Observation, self).create(vals)

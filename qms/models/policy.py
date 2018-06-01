# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Policy(models.Model):

    _name = "qms.policy"

    name = fields.Char(
        required=True
    )

    version = fields.Integer()

    date = fields.Date()

    last_review_date = fields.Date(compute='_compute_last_review_date')

    approved = fields.Boolean()

    description = fields.Html()

    policy_component_ids = fields.Many2many(
        comodel_name='qms.policy_component',
        required=True
    )

    review_ids = fields.One2many(
        comodel_name='qms.review',
        inverse_name='policy_id'
    )

    @api.multi
    @api.depends('review_ids')
    def _compute_last_review_date(self):
        for policy in self:
            domain = [
                ('policy_id', '=', policy.id),
                #('modify_concession', '=', True)
            ]
            related_reviews = policy.env['qms.review'].search(domain)
            last_review = related_reviews.sorted(
                key=lambda r: r.date,
                reverse=True)
            policy.last_review_date = last_review[0].date


    @api.one
    def toggle_approved(self):
        self.approved = not self.approved

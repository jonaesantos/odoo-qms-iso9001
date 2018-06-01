# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Hazard(models.Model):

    _name = "qms.hazard"

    _probabilities_ = [
        (1, 'Very Low (Rare)'),
        (2, 'Low (Improbable)'),
        (3, 'Medium (Possible)'),
        (4, 'High Medium (Probable)'),
        (5, 'Very High (Almost Sure)')
    ]

    _impacts_ = [
        (1, 'Very Low (Rare)'),
        (2, 'Low (Improbable)'),
        (3, 'Medium (Possible)'),
        (4, 'High Medium (Probable)'),
        (5, 'Very High (Almost Sure)')
    ]

    _strategies_ = [
        ('accept', 'Accept'),
        ('watch', 'Watch'),
        ('evitar', 'Avoid'),
        ('transfer', 'Transfer'),
        ('reduce', 'Reduce'),
        ('share', 'Share'),
        ('palliate', 'Palliate')
    ]

    _states_ = [
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled')
    ]

    _evaluation_results_ = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('very_high', 'Very High')
    ]

    @api.one
    @api.depends('probability',
                 'impact')
    def _compute_result_and_evaluation(self):
        if self.impact and self.probability:
            self.result = self.impact * self.probability
        else:
            self.result = 0
        if self.result >= 1 and self.result <= 3:
            self.evaluation = 'low'
        elif self.result >= 4 and self.result <= 8:
            self.evaluation = 'medium'
        elif self.result >= 9 and self.result <= 14:
            self.evaluation = 'high'
        elif self.result >= 15 and self.result <= 25:
            self.evaluation = 'very_high'
        else:
            self.evaluation = False

    name = fields.Char(
        required=True
    )

    date = fields.Date()

    probability = fields.Selection(
        selection=_probabilities_,
        required=True
    )

    impact = fields.Selection(
        selection=_impacts_,
        required=True
    )

    strategy = fields.Selection(
        selection=_strategies_,
        required=True
    )

    state = fields.Selection(
        selection=_states_,
        default='draft',
        required=True
    )

    evaluation = fields.Selection(
        selection=_evaluation_results_,
        compute=_compute_result_and_evaluation,
        readonly=True
    )

    result = fields.Integer(
        compute=_compute_result_and_evaluation,
        readonly=True
    )

    process_ids = fields.Many2many(
        comodel_name='qms.process',
        required=True
    )

    policy_component_ids = fields.Many2many(
        comodel_name='qms.policy_component',
        required=True
    )

    action_ids = fields.Many2many(
        comodel_name='qms.action'
    )

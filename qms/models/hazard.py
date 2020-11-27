
from odoo import api, fields, models, _


class Hazard(models.Model):

    _name = "qms.hazard"

    _description = "Action"

    number = fields.Integer()

    _probabilities_ = [
        (1, 'Very Low (Rare)'),
        (2, 'Low (Improbable)'),
        (3, 'Medium (Possible)'),
        (4, 'High Medium (Probable)'),
        (5, 'Very High (Almost Sure)')
    ]

    _impacts_ = [
        (1, 'Very Low (Insignificant)'),
        (2, 'Low (Less)'),
        (3, 'Medium (Moderate)'),
        (4, 'High Medium (Higher)'),
        (5, 'Very High (Catastrophic)')
    ]

    _strategies_ = [
        ('accept', 'Accept'),
        ('watch', 'Watch'),
        ('evitar', 'Avoid'),
        ('transfer', 'Transfer'),
        ('reduce', 'Reduce'),
        ('share', 'Share'),
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

    _complexity_levels_ = [
        ('very_low', 'Very Low'),
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('very_high', 'Very High')
    ]

    _types_risks_ = [
        ('strategic', 'Estratégico'),
        ('image', 'Imagen'),
        ('operative', 'Operativo'),
        ('financial', 'Financiero'),
        ('compliance', 'Cumplimiento'),
        ('technological', 'Tecnológico'),
        ('corruption', 'Corrupción'),
        ('information', 'Información')
    ]

    _factors_ = [
        ('e_economic', 'Económicos (e)'),
        ('e_politicians', 'Políticos (e)'),
        ('e_social', 'Sociales (e)'),
        ('e_technological', 'Tecnológicos (e)'),
        ('e_enviroment', 'Ambientales (e)'),
        ('e_communication', 'Comunicación (e)'),
        ('i_financial', 'Financiero (i)'),
        ('i_personal', 'Personal (i)'),
        ('i_technological', 'Procesos (i)'),
        ('i_strategic', 'Tecnológicos (i)'),
        ('i_communication', 'Estratégicos (i)'),
        ('i_factors', 'Comunicación (i)')
    ]

    description = fields.Html()

    causes = fields.Html()

    consequences = fields.Html()

    type_risk = fields.Selection(
        selection=_types_risks_,
        required=False
    )

    factor = fields.Selection(
        selection=_factors_,
        required=False
    )

    
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
        required=False
    )

    impact = fields.Selection(
        selection=_impacts_,
        required=False
    )

    strategy = fields.Selection(
        selection=_strategies_,
        required=False
    )

    state = fields.Selection(
        selection=_states_,
        default='draft',
        required=False
    )

    evaluation = fields.Selection(
        selection=_evaluation_results_,
        compute=_compute_result_and_evaluation,
        readonly=True
    )

    result = fields.Integer(
        compute=_compute_result_and_evaluation,
        readonly=True,
        store=True
    )

    process_ids = fields.Many2many(
        comodel_name='qms.process',
        required=False
    )

    policy_component_ids = fields.Many2many(
        comodel_name='qms.policy_component',
        required=False
    )

    action_ids = fields.One2many(
        comodel_name='qms.action',
        inverse_name='hazard_id'
    )

    review_ids = fields.One2many(
        comodel_name='qms.review',
        inverse_name='hazard_id',
    )

    last_review_date = fields.Date(compute='_compute_last_review_date')

    
    @api.depends('review_ids')
    def _compute_last_review_date(self):
        for hazard in self:
            domain = [
                ('hazard_id', '=', hazard.id),
                #('modify_concession', '=', True)
            ]
            related_reviews = hazard.env['qms.review'].search(domain)
            last_review = related_reviews.sorted(
                key=lambda r: r.date,
                reverse=True)
            hazard.last_review_date = last_review[0].date


    _sql_constraints = [
        ('number_uniq', 'unique(number)', 'Number must be unique'),
    ]

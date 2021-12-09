from odoo import _, api, fields, models


class Hazard(models.Model):

    _name = "qms.hazard"
    _description = "Hazard"

    number = fields.Integer()

    _probabilities_ = [
        ("1", _("Very Low (Rare)")),
        ("2", _("Low (Improbable)")),
        ("3", _("Medium (Possible)")),
        ("4", _("High Medium (Probable)")),
        ("5", _("Very High (Almost Sure)")),
    ]

    _impacts_ = [
        ("1", _("Very Low (Insignificant)")),
        ("2", _("Low (Less)")),
        ("3", _("Medium (Moderate)")),
        ("4", _("High Medium (Higher)")),
        ("5", _("Very High (Catastrophic)")),
    ]

    _strategies_ = [
        ("accept", _("Accept")),
        ("watch", _("Watch")),
        ("evitar", _("Avoid")),
        ("transfer", _("Transfer")),
        ("reduce", _("Reduce")),
        ("share", _("Share")),
    ]

    _states_ = [
        ("draft", _("Draft")),
        ("open", _("Open")),
        ("closed", _("Closed")),
        ("cancelled", _("Cancelled")),
    ]

    _evaluation_results_ = [
        ("low", _("Low")),
        ("medium", _("Medium")),
        ("high", _("High")),
        ("very_high", _("Very High")),
    ]

    _complexity_levels_ = [
        ("very_low", _("Very Low")),
        ("low", _("Low")),
        ("medium", _("Medium")),
        ("high", _("High")),
        ("very_high", _("Very High")),
    ]

    _types_risks_ = [
        ("strategic", _("Strategic")),
        ("image", _("Image")),
        ("operative", _("Operative")),
        ("financial", _("Financial")),
        ("compliance", _("Compliance")),
        ("technological", _("Technological")),
        ("corruption", _("Corruption")),
        ("information", _("Information")),
    ]

    _factors_ = [
        ("e_economic", _("Economics (external)")),
        ("e_politicians", _("Politicians (external)")),
        ("e_social", _("Social (external)")),
        ("e_technological", _("Technological (external)")),
        ("e_enviroment", _("Enviroment (external)")),
        ("e_communication", _("Communication (external)")),
        ("i_financial", _("Financial (internal)")),
        ("i_personal", _("Personal (internal)")),
        ("i_technological", _("Technological (internal)")),
        ("i_strategic", _("Srategic (internal)")),
        ("i_communication", _("Communication (internal)")),
        ("i_factors", _("Factors (internal)")),
    ]

    description = fields.Html()

    causes = fields.Html()

    consequences = fields.Html()

    type_risk = fields.Selection(selection=_types_risks_, required=False)

    factor = fields.Selection(selection=_factors_, required=False)

    @api.depends("probability", "impact")
    def _compute_result_and_evaluation(self):
        if self.impact and self.probability:
            self.result = self.impact * self.probability
        else:
            self.result = 0
        if self.result >= 1 and self.result <= 3:
            self.evaluation = "low"
        elif self.result >= 4 and self.result <= 8:
            self.evaluation = "medium"
        elif self.result >= 9 and self.result <= 14:
            self.evaluation = "high"
        elif self.result >= 15 and self.result <= 25:
            self.evaluation = "very_high"
        else:
            self.evaluation = False

    name = fields.Char(required=True)

    date = fields.Date()

    probability = fields.Selection(selection=_probabilities_, required=False)

    impact = fields.Selection(selection=_impacts_, required=False)

    strategy = fields.Selection(selection=_strategies_, required=False)

    state = fields.Selection(
        selection=_states_, default="draft", required=False
    )

    evaluation = fields.Selection(
        selection=_evaluation_results_,
        compute=_compute_result_and_evaluation,
        readonly=True,
        compute_sudo=True,
    )

    result = fields.Integer(
        compute=_compute_result_and_evaluation,
        readonly=True,
        store=True,
        compute_sudo=True,
    )

    process_ids = fields.Many2many(comodel_name="qms.process", required=False)

    policy_component_ids = fields.Many2many(
        comodel_name="qms.policy_component", required=False
    )

    action_ids = fields.One2many(
        comodel_name="qms.action", inverse_name="hazard_id"
    )

    review_ids = fields.One2many(
        comodel_name="qms.review", inverse_name="hazard_id"
    )

    last_review_date = fields.Date(compute="_compute_last_review_date")

    @api.depends("review_ids")
    def _compute_last_review_date(self):
        for hazard in self:
            domain = [
                ("hazard_id", "=", hazard.id),
                # ('modify_concession', '=', True)
            ]
            related_reviews = hazard.env["qms.review"].search(domain)
            last_review = related_reviews.sorted(
                key=lambda r: r.date, reverse=True
            )
            hazard.last_review_date = last_review[0].date

    _sql_constraints = [
        ("number_uniq", "unique(number)", "Number must be unique")
    ]

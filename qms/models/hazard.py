from odoo import _, api, fields, models


class Hazard(models.Model):

    _name = "qms.hazard"
    _description = "Hazard"

    number = fields.Char(
        string="Risk Number",
        copy=False,
        readonly=True,
    )

    description = fields.Html()

    causes = fields.Html()

    consequences = fields.Html()

    type_risk = fields.Selection(
        selection=[
            ("strategic", "Strategic"),
            ("image", "Image"),
            ("operative", "Operative"),
            ("financial", "Financial"),
            ("compliance", "Compliance"),
            ("technological", "Technological"),
            ("corruption", "Corruption"),
            ("information", "Information"),
        ],
        required=False,
    )

    factor = fields.Selection(
        selection=[
            ("e_economic", "Economics (external)"),
            ("e_politicians", "Politicians (external)"),
            ("e_social", "Social (external)"),
            ("e_technological", "Technological (external)"),
            ("e_enviroment", "Enviroment (external)"),
            ("e_communication", "Communication (external)"),
            ("i_financial", "Financial (internal)"),
            ("i_personal", "Personal (internal)"),
            ("i_technological", "Technological (internal)"),
            ("i_strategic", "Srategic (internal)"),
            ("i_communication", "Communication (internal)"),
            ("i_factors", "Factors (internal)"),
        ],
        required=False,
    )

    @api.depends("probability", "impact")
    def _compute_result_and_evaluation(self):
        for hazard in self:
            if hazard.impact and hazard.probability:
                hazard.result = int(hazard.impact) * int(hazard.probability)
            else:
                hazard.result = 0

            if hazard.result >= 1 and hazard.result <= 3:
                hazard.evaluation = "low"
            elif hazard.result >= 4 and hazard.result <= 8:
                hazard.evaluation = "medium"
            elif hazard.result >= 9 and hazard.result <= 14:
                hazard.evaluation = "high"
            elif hazard.result >= 15 and hazard.result <= 25:
                hazard.evaluation = "very_high"
            else:
                hazard.evaluation = False

    name = fields.Char(required=True)

    date = fields.Date()

    probability = fields.Selection(
        selection=[
            ("1", "Very Low (Rare)"),
            ("2", "Low (Improbable)"),
            ("3", "Medium (Possible)"),
            ("4", "High Medium (Probable)"),
            ("5", "Very High (Almost Sure)"),
        ],
        required=False,
    )

    impact = fields.Selection(
        selection=[
            ("1", "Very Low (Insignificant)"),
            ("2", "Low (Less)"),
            ("3", "Medium (Moderate)"),
            ("4", "High Medium (Higher)"),
            ("5", "Very High (Catastrophic)"),
        ],
        required=False,
    )

    strategy = fields.Selection(
        selection=[
            ("accept", "Accept"),
            ("watch", "Watch"),
            ("evitar", "Avoid"),
            ("transfer", "Transfer"),
            ("reduce", "Reduce"),
            ("share", "Share"),
        ],
        required=False,
    )

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("open", "Open"),
            ("closed", "Closed"),
            ("cancelled", "Cancelled"),
        ],
        default="draft",
        required=False,
    )

    evaluation = fields.Selection(
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
            ("very_high", "Very High"),
        ],
        compute=_compute_result_and_evaluation,
        readonly=True,
        store=True,
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

    last_review_date = fields.Date(compute="_compute_last_review_date", store=True)

    @api.depends("review_ids.date")
    def _compute_last_review_date(self):
        for hazard in self:
            if hazard.review_ids:
                last_review = hazard.review_ids.sorted(
                    key=lambda r: r.date, reverse=True
                )
                hazard.last_review_date = last_review[0].date
            else:
                hazard.last_review_date = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("number"):
                vals["number"] = self.env["ir.sequence"].next_by_code("qms.hazard")
        return super(Hazard, self).create(vals_list)

    _sql_constraints = [
        ("unique_number", "UNIQUE(number)", "Number must be unique")
    ]

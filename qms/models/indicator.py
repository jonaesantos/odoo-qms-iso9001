from odoo import _, api, fields, models


class Indicator(models.Model):

    _name = "qms.indicator"
    _description = "Indicator"

    name = fields.Char(required=True)

    number = fields.Integer()

    _resource_states_ = [
        ("enabled", _("Enabled")),
        ("disabled", _("Disabled")),
    ]

    _frequencys_ = [
        ("annual", _("Annual")),
        ("biannual", _("Biannual")),
        ("quarterly", _("Quarterly")),
        ("monthly", _("Monthly")),
    ]

    responsible_id = fields.Many2one(
        comodel_name="qms.interested_party", required=True
    )

    review_ids = fields.One2many(
        comodel_name="qms.review", inverse_name="indicator_id"
    )

    state = fields.Selection(selection=_resource_states_, default="enabled")

    frequency = fields.Selection(selection=_frequencys_, default="annual")

    process_id = fields.Many2one(comodel_name="qms.process", required=True)

    measurement_ids = fields.One2many(
        comodel_name="qms.indicator.measurement", inverse_name="indicator_id"
    )

    version_ids = fields.One2many(
        comodel_name="qms.version", inverse_name="indicator_id"
    )

    non_conformity_ids = fields.One2many(
        comodel_name="qms.non_conformity", inverse_name="indicator_id"
    )

    observation_ids = fields.One2many(
        comodel_name="qms.observation", inverse_name="indicator_id"
    )

    opportunity_ids = fields.One2many(
        comodel_name="qms.opportunity", inverse_name="indicator_id"
    )

    description = fields.Html(string="Objetive")

    last_measurement_date = fields.Date(
        compute="_compute_last_measurement_date"
    )

    last_measurement_result = fields.Char(
        compute="_compute_last_measurement_result", store=True
    )

    last_measurement_result_detail = fields.Char(
        compute="_compute_last_measurement_result_detail"
    )

    last_review_date = fields.Date(compute="_compute_last_review_date")

    @api.depends("measurement_ids")
    def _compute_last_measurement_date(self):
        for indicator in self:
            domain = [
                ("indicator_id", "=", indicator.id),
            ]
            related_measurement = indicator.env[
                "qms.indicator.measurement"
            ].search(domain)
            last_measurement = related_measurement.sorted(
                key=lambda r: r.measurement_date, reverse=True
            )
            indicator.last_measurement_date = last_measurement[
                0
            ].measurement_date

    @api.depends("measurement_ids")
    def _compute_last_measurement_result(self):
        for indicator in self:
            domain = [
                ("indicator_id", "=", indicator.id),
            ]
            related_measurement = indicator.env[
                "qms.indicator.measurement"
            ].search(domain)
            last_measurement = related_measurement.sorted(
                key=lambda r: r.measurement_date, reverse=True
            )
            indicator.last_measurement_result = last_measurement[0].result

    @api.depends("measurement_ids")
    def _compute_last_measurement_result_detail(self):
        for indicator in self:
            domain = [
                ("indicator_id", "=", indicator.id),
            ]
            related_measurement = indicator.env[
                "qms.indicator.measurement"
            ].search(domain)
            last_measurement = related_measurement.sorted(
                key=lambda r: r.measurement_date, reverse=True
            )
            indicator.last_measurement_result_detail = last_measurement[
                0
            ].result_detail

    @api.depends("review_ids")
    def _compute_last_review_date(self):
        for indicator in self:
            domain = [
                ("indicator_id", "=", indicator.id),
            ]
            related_reviews = indicator.env["qms.review"].search(domain)
            last_review = related_reviews.sorted(
                key=lambda r: r.date, reverse=True
            )
            indicator.last_review_date = last_review[0].date

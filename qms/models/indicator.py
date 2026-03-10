from odoo import _, api, fields, models


class Indicator(models.Model):

    _name = "qms.indicator"
    _description = "Indicator"

    name = fields.Char(required=True)

    number = fields.Integer()

    responsible_id = fields.Many2one(
        comodel_name="qms.interested_party", required=True, ondelete="restrict"
    )

    review_ids = fields.One2many(
        comodel_name="qms.review", inverse_name="indicator_id"
    )

    state = fields.Selection(
        selection=[
            ("enabled", "Enabled"),
            ("disabled", "Disabled"),
        ],
        default="enabled",
    )

    frequency = fields.Selection(
        selection=[
            ("annual", "Annual"),
            ("biannual", "Biannual"),
            ("quarterly", "Quarterly"),
            ("monthly", "Monthly"),
        ],
        default="annual",
    )

    process_id = fields.Many2one(comodel_name="qms.process", required=True, ondelete="restrict")

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
        compute="_compute_last_measurement_date", store=True
    )

    last_measurement_result = fields.Char(
        compute="_compute_last_measurement_result", store=True
    )

    last_measurement_result_detail = fields.Char(
        compute="_compute_last_measurement_result_detail", store=True
    )

    last_review_date = fields.Date(compute="_compute_last_review_date")

    @api.depends("measurement_ids.measurement_date")
    def _compute_last_measurement_date(self):
        for indicator in self:
            if indicator.measurement_ids:
                last_measurement = indicator.measurement_ids.sorted(
                    key=lambda r: r.measurement_date, reverse=True
                )
                indicator.last_measurement_date = last_measurement[0].measurement_date
            else:
                indicator.last_measurement_date = False

    @api.depends("measurement_ids.measurement_date", "measurement_ids.result")
    def _compute_last_measurement_result(self):
        for indicator in self:
            if indicator.measurement_ids:
                last_measurement = indicator.measurement_ids.sorted(
                    key=lambda r: r.measurement_date, reverse=True
                )
                indicator.last_measurement_result = last_measurement[0].result
            else:
                indicator.last_measurement_result = False

    @api.depends("measurement_ids.measurement_date", "measurement_ids.result_detail")
    def _compute_last_measurement_result_detail(self):
        for indicator in self:
            if indicator.measurement_ids:
                last_measurement = indicator.measurement_ids.sorted(
                    key=lambda r: r.measurement_date, reverse=True
                )
                indicator.last_measurement_result_detail = last_measurement[0].result_detail
            else:
                indicator.last_measurement_result_detail = False

    @api.depends("review_ids.date")
    def _compute_last_review_date(self):
        for indicator in self:
            if indicator.review_ids:
                last_review = indicator.review_ids.sorted(
                    key=lambda r: r.date, reverse=True
                )
                indicator.last_review_date = last_review[0].date
            else:
                indicator.last_review_date = False

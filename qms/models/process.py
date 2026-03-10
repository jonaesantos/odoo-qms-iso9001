from odoo import api, fields, models


class Process(models.Model):

    _name = "qms.process"
    _description = "Process"

    name = fields.Char(required=True)

    responsible_id = fields.Many2one(
        comodel_name="qms.interested_party", required=True, ondelete="restrict"
    )

    review_ids = fields.One2many(
        comodel_name="qms.review", inverse_name="process_id"
    )

    resource_ids = fields.Many2many(comodel_name="qms.resource")

    resource_type = fields.Selection(
        selection=[
            ("strategic", "Strategic"),
            ("central", "Central"),
            ("support", "Support"),
        ]
    )

    state = fields.Selection(
        selection=[
            ("enabled", "Enabled"),
            ("disabled", "Disabled"),
        ],
        default="enabled",
    )

    indicator_ids = fields.One2many(
        comodel_name="qms.indicator", inverse_name="process_id", required=False
    )

    policy_component_ids = fields.Many2many(
        comodel_name="qms.policy_component", required=True
    )

    description = fields.Html()

    inputs = fields.Html()

    outputs = fields.Html()

    last_review_date = fields.Date(compute="_compute_last_review_date", store=True)

    indicator_count = fields.Integer(
        string="Indicators",
        compute="_compute_indicator_count",
        store=True,
    )

    @api.depends("review_ids.date")
    def _compute_last_review_date(self):
        for process in self:
            if process.review_ids:
                last_review = process.review_ids.sorted(
                    key=lambda r: r.date, reverse=True
                )
                process.last_review_date = last_review[0].date
            else:
                process.last_review_date = False

    @api.depends("indicator_ids")
    def _compute_indicator_count(self):
        for process in self:
            process.indicator_count = len(process.indicator_ids)
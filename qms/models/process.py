from odoo import _, api, fields, models


class Process(models.Model):

    _name = "qms.process"
    _description = "Process"

    name = fields.Char(required=True)

    _resource_types_ = [
        ("strategic", _("Strategic")),
        ("central", _("Central")),
        ("support", _("Support")),
    ]

    _resource_states_ = [
        ("enabled", _("Enabled")),
        ("disabled", _("Disabled")),
    ]

    responsible_id = fields.Many2one(
        comodel_name="qms.interested_party", required=False
    )

    review_ids = fields.One2many(
        comodel_name="qms.review", inverse_name="process_id"
    )

    resource_ids = fields.Many2many(comodel_name="qms.resource")

    resource_type = fields.Selection(selection=_resource_types_)

    state = fields.Selection(selection=_resource_states_, default="enabled")

    indicator_ids = fields.One2many(
        comodel_name="qms.indicator", inverse_name="process_id", required=False
    )

    policy_component_ids = fields.Many2many(
        comodel_name="qms.policy_component", required=True
    )

    description = fields.Html()

    inputs = fields.Html()

    outputs = fields.Html()

    last_review_date = fields.Date(compute="_compute_last_review_date")

    @api.depends("review_ids")
    def _compute_last_review_date(self):
        for process in self:
            domain = [
                ("process_id", "=", process.id),
            ]
            related_reviews = process.env["qms.review"].search(domain)
            last_review = related_reviews.sorted(
                key=lambda r: r.date, reverse=True
            )
            process.last_review_date = last_review[0].date

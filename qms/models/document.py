from odoo import api, fields, models


class Document(models.Model):

    _name = "qms.document"
    _description = "Document"

    identification = fields.Char(required=True)

    name = fields.Char(required=True)

    format = fields.Selection(
        selection=[
            ("paper", "Paper"),
            ("electronic", "Electronic"),
        ],
        default="electronic",
        required=True,
    )

    version_ids = fields.One2many(
        comodel_name="qms.version", inverse_name="document_id"
    )

    relation = fields.Selection(
        selection=[
            ("sgc&tmc", "SGC / TMC"),
            ("sgc", "SGC"),
            ("tmc", "TMC"),
        ],
        default="sgc&tmc",
        required=True,
    )

    holding_time = fields.Char()

    storage = fields.Char()

    link = fields.Html()

    disposition = fields.Char()

    type = fields.Selection(
        selection=[
            ("internal", "Internal"),
            ("external", "External"),
        ],
        default="internal",
        required=True,
    )

    description = fields.Html()

    responsible_id = fields.Many2one(
        comodel_name="qms.interested_party", required=True, ondelete="restrict"
    )

    process_ids = fields.Many2many(comodel_name="qms.process", required=True)

    review_ids = fields.One2many(
        comodel_name="qms.review", inverse_name="document_id"
    )

    approved = fields.Boolean()

    last_review_date = fields.Date(compute="_compute_last_review_date", store=True)

    last_version = fields.Char(compute="_compute_last_version", store=True)

    @api.depends("review_ids.date")
    def _compute_last_review_date(self):
        for document in self:
            if document.review_ids:
                last_review = document.review_ids.sorted(
                    key=lambda r: r.date, reverse=True
                )
                document.last_review_date = last_review[0].date
            else:
                document.last_review_date = False

    @api.depends("version_ids.date_open", "version_ids.version")
    def _compute_last_version(self):
        for document in self:
            if document.version_ids:
                last_version = document.version_ids.sorted(
                    key=lambda r: r.date_open, reverse=True
                )
                document.last_version = last_version[0].version
            else:
                document.last_version = False

    def action_toggle_approved(self):
        self.approved = not self.approved

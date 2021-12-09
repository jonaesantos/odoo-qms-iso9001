from odoo import _, api, fields, models


class Document(models.Model):

    _name = "qms.document"
    _description = "Document"

    identification = fields.Char(required=True)

    name = fields.Char()

    _format_ = [("paper", ("Paper")), ("electronic", _("Electronic"))]

    format = fields.Selection(
        selection=_format_, default="electronic", required=True
    )

    version_ids = fields.One2many(
        comodel_name="qms.version", inverse_name="document_id"
    )

    _relation_ = [("sgc&tmc", "SGC / TMC"), ("sgc", "SGC"), ("tmc", "TMC")]

    relation = fields.Selection(
        selection=_relation_, default="sgc&tmc", required=True
    )

    holding_time = fields.Char()

    storage = fields.Char()

    link = fields.Char()

    disposition = fields.Char()

    _type_ = [("internal", _("Internal")), ("external", _("External"))]

    type = fields.Selection(
        selection=_type_, default="internal", required=True
    )

    description = fields.Html()

    responsible_id = fields.Many2one(
        comodel_name="qms.interested_party", required=True
    )

    process_ids = fields.Many2many(comodel_name="qms.process", required=True)

    review_ids = fields.One2many(
        comodel_name="qms.review", inverse_name="document_id"
    )

    approved = fields.Boolean()

    last_review_date = fields.Date(compute="_compute_last_review_date")

    last_version = fields.Char(compute="_compute_last_version")

    @api.depends("review_ids")
    def _compute_last_review_date(self):
        for document in self:
            domain = [
                ("document_id", "=", document.id),
            ]
            related_reviews = document.env["qms.review"].search(domain)
            last_review = related_reviews.sorted(
                key=lambda r: r.date, reverse=True
            )
            document.last_review_date = last_review[0].date

    @api.depends("version_ids")
    def _compute_last_version(self):
        for document in self:
            domain = [
                ("document_id", "=", document.id),
            ]
            related_versions = document.env["qms.version"].search(domain)
            last_version = related_versions.sorted(
                key=lambda r: r.date_open, reverse=True
            )
            document.last_version = last_version[0].version

    def toggle_approved(self):
        self.approved = not self.approved

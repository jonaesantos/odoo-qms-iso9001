from odoo import _, api, fields, models


class InterestedParty(models.Model):

    _name = "qms.interested_party"
    _description = "Interested Party"

    _interested_party_types_ = [
        ("internal", _("Internal")),
        ("external", _("External")),
    ]

    _power_ = [
        ("1", _("Low")),
        ("2", _("Medium")),
        ("3", _("High")),
        ("4", _("Very High")),
    ]

    _interest_ = [
        ("1", _("Low")),
        ("2", _("Medium")),
        ("3", _("High")),
        ("4", _("Very High")),
    ]

    _cooperation_ = [
        ("1", _("Low")),
        ("2", _("Medium")),
        ("3", _("High")),
        ("4", _("Very High")),
    ]

    _impact_ = [
        ("1", _("Low")),
        ("2", _("Medium")),
        ("3", _("High")),
        ("4", _("Very High")),
    ]

    power = fields.Selection(selection=_power_, required=False)

    interest = fields.Selection(selection=_interest_, required=False)

    cooperation = fields.Selection(selection=_cooperation_, required=False)

    impact = fields.Selection(selection=_impact_, required=False)

    name = fields.Char(required=True)

    interested_party_type = fields.Selection(
        selection=_interested_party_types_
    )

    is_organization = fields.Boolean()

    organization_id = fields.Many2one(
        comodel_name="qms.interested_party",
        domain=[("is_organization", "=", True)],
    )

    requeriments_interested_party = fields.Html()

    interest_tmc = fields.Html()

    area = fields.Char()

    review_ids = fields.One2many(
        comodel_name="qms.review", inverse_name="interested_party_id"
    )

    last_review_date = fields.Date(compute="_compute_last_review_date")

    @api.depends("review_ids")
    def _compute_last_review_date(self):
        for interested_party in self:
            domain = [("interested_party_id", "=", interested_party.id)]
            related_reviews = interested_party.env["qms.review"].search(domain)
            last_review = related_reviews.sorted(
                key=lambda r: r.date, reverse=True
            )
            interested_party.last_review_date = last_review[0].date

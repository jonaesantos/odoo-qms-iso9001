from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class RevisionByDirection(models.Model):

    _name = "qms.revision_by_direction"
    _description = "Revision by Direction"

    name = fields.Char(required=True)

    description = fields.Html()

    date_open = fields.Datetime()

    date_close = fields.Datetime()

    resource_ids = fields.Many2many(comodel_name="qms.resource")

    non_conformity_ids = fields.One2many(
        comodel_name="qms.non_conformity",
        inverse_name="revision_by_direction_id",
    )

    observation_ids = fields.One2many(
        comodel_name="qms.observation", inverse_name="revision_by_direction_id"
    )

    opportunity_ids = fields.One2many(
        comodel_name="qms.opportunity", inverse_name="revision_by_direction_id"
    )

    action_ids = fields.One2many(
        comodel_name="qms.action",
        inverse_name="revision_by_direction_id"
        # ondelete="cascade",
    )

    # responsibles_ids = fields.Many2many(
    #     comodel_name="qms.interested_party",
    #     relation="audit_auditor_rel",
    #     ondelete="cascade",
    # )

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("open", "Open"),
            ("done", "Closed"),
        ],
        default="draft",
    )

    def button_close(self):
        self.write(
            {"state": "done", "date_close": fields.Datetime.now()}
        )
        return True

    @api.constrains("date_open", "date_close")
    def _check_dates(self):
        for revision in self:
            if revision.date_close and revision.date_open:
                if revision.date_close < revision.date_open:
                    raise ValidationError(
                        _("Close date must be after open date")
                    )

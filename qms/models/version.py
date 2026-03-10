from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Version(models.Model):

    _name = "qms.version"
    _description = "Version"

    version = fields.Char()

    change_history = fields.Html()

    date_open = fields.Date()

    document_id = fields.Many2one(
        comodel_name="qms.document", ondelete="cascade"
    )

    policy_id = fields.Many2one(comodel_name="qms.policy", ondelete="cascade")

    indicator_id = fields.Many2one(
        comodel_name="qms.indicator", ondelete="cascade"
    )

    procedure_id = fields.Many2one(
        comodel_name="qms.procedure", ondelete="cascade"
    )

    instructive_id = fields.Many2one(
        comodel_name="qms.instructive", ondelete="cascade"
    )

    registry_id = fields.Many2one(
        comodel_name="qms.registry", ondelete="cascade"
    )

    responsible_id = fields.Many2one(
        comodel_name="qms.interested_party", required=True, ondelete="restrict"
    )

    @api.constrains(
        "document_id",
        "policy_id",
        "indicator_id",
        "procedure_id",
        "instructive_id",
        "registry_id",
    )
    def _check_parent_reference(self):
        for version in self:
            if not any(
                [
                    version.document_id,
                    version.policy_id,
                    version.indicator_id,
                    version.procedure_id,
                    version.instructive_id,
                    version.registry_id,
                ]
            ):
                raise ValidationError(
                    _(
                        "Version must be associated with at least one parent record "
                        "(Policy, Document, Indicator, Procedure, Instructive, or Registry)"
                    )
                )

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class EffectivenessCheck(models.Model):

    _name = "qms.effectiveness_check"
    _description = "Effectiveness Check"

    _states_ = [("pending", _("Pending")), ("closed", _("Closed"))]

    expected_date = fields.Date()

    verification_date = fields.Date()

    was_effective = fields.Boolean()

    action_id = fields.Many2one(comodel_name="qms.action", required=True)

    state = fields.Selection(selection=_states_, default="pending")

    observations = fields.Text()

    @api.constrains("state")
    def _check_closed_with_verification_date(self):
        for effectiveness_check in self:
            if (
                effectiveness_check.state == "closed"
                and not effectiveness_check.verification_date
            ):
                raise ValidationError(
                    _(
                        "Verification_date are required in order to put a \
                        effectiveness_check 'closed'"
                    )
                )

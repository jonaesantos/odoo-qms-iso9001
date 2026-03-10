from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Action(models.Model):

    _name = "qms.action"
    _description = "Action"

    def _default_stage(self):
        return self.env["qms.action.stage"].search(
            [("is_starting", "=", True)], limit=1
        )

    name = fields.Char(required=True)

    active = fields.Boolean(default=True)

    date_deadline = fields.Date()

    create_date = fields.Date(readonly=True, default=fields.Date.today)

    cancel_date = fields.Date(readonly=True)

    opening_date = fields.Datetime(readonly=False)

    date_closed = fields.Datetime(readonly=False)

    description = fields.Html()

    response_type = fields.Selection(
        selection=[
            ("improvement", "Improvement Action"),
            ("immediate", "Immediate Action"),
            ("correction", "Corrective Action"),
            ("preventive", "Action for Risks"),
        ],
        required=True,
    )

    stage_id = fields.Many2one(
        comodel_name="qms.action.stage",
        copy=False,
        index=True,
        default=_default_stage,
        group_expand="_stage_groups",
        ondelete="restrict",
    )

    color = fields.Integer(related="stage_id.color", store=False)

    reference = fields.Char(required=False, readonly=True)

    complexity = fields.Selection(
        selection=[
            ("very_low", "Very Low"),
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
            ("very_high", "Very High"),
        ],
        required=True,
    )

    responsible_id = fields.Many2one(
        comodel_name="qms.interested_party", required=True, ondelete="restrict"
    )

    effectiveness_check_ids = fields.One2many(
        comodel_name="qms.effectiveness_check",
        inverse_name="action_id",
        required=False,
    )

    observation_id = fields.Many2one(comodel_name="qms.observation", ondelete="set null")

    non_conformity_id = fields.Many2one(comodel_name="qms.non_conformity", ondelete="set null")

    complaint_id = fields.Many2one(comodel_name="qms.complaint", ondelete="set null")

    opportunity_id = fields.Many2one(comodel_name="qms.opportunity", ondelete="set null")

    hazard_id = fields.Many2one(comodel_name="qms.hazard", ondelete="set null")

    goal_id = fields.Many2one(comodel_name="qms.goal", ondelete="set null")

    revision_by_direction_id = fields.Many2one(
        comodel_name="qms.revision_by_direction", ondelete="set null"
    )

    @api.model_create_multi
    def create(self, vals_list):
        seq = self.env["ir.sequence"]
        for vals in vals_list:
            vals["reference"] = seq.next_by_code("qms.action")
        return super(Action, self).create(vals_list)

    @api.model
    def _stage_groups(self, stages, domain):
        return self.env["qms.action.stage"].search([])

    @api.model
    def _get_stage_new(self):
        return self.env["qms.action.stage"].search([])

    @api.constrains("opening_date", "date_closed")
    def _check_dates(self):
        for action in self:
            if action.date_closed and action.opening_date:
                if action.date_closed < action.opening_date:
                    raise ValidationError(
                        _("Close date must be after opening date")
                    )

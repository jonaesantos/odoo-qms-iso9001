# This model is based in some code used in OCA Management System Addons Project
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class Action(models.Model):

    _name = "qms.action"
    _description = "Action"

    _response_types_ = [
        ("improvement", _("Improvement Action")),
        ("immediate", _("Immediate Action")),
        ("correction", _("Corrective Action")),
        ("preventive", _("Action for Risks")),
    ]

    _complexity_levels_ = [
        ("very_low", _("Very Low")),
        ("low", _("Low")),
        ("medium", _("Medium")),
        ("high", _("High")),
        ("very_high", _("Very High")),
    ]

    def _default_stage(self):
        return self.env["qms.action.stage"].search(
            [("is_starting", "=", True)], limit=1
        )

    name = fields.Char(required=True)

    active = fields.Boolean(default=True)

    date_deadline = fields.Date()

    create_date = fields.Date(readonly=True, default=fields.datetime.now())

    cancel_date = fields.Date(readonly=True)

    opening_date = fields.Date(readonly=False)

    date_closed = fields.Date(readonly=False)

    description = fields.Html()

    response_type = fields.Selection(selection=_response_types_, required=True)

    stage_id = fields.Many2one(
        comodel_name="qms.action.stage",
        copy=False,
        index=True,
        default=_default_stage,
        group_expand="_stage_groups",
    )

    reference = fields.Char(required=False, readonly=True)

    complexity = fields.Selection(selection=_complexity_levels_, required=True)

    responsible_id = fields.Many2one(
        comodel_name="qms.interested_party", required=True
    )

    effectiveness_check_ids = fields.One2many(
        comodel_name="qms.effectiveness_check",
        inverse_name="action_id",
        required=False,
    )

    observation_id = fields.Many2one(comodel_name="qms.finding")

    non_conformity_id = fields.Many2one(comodel_name="qms.finding")

    complaint_id = fields.Many2one(comodel_name="qms.finding")

    opportunity_id = fields.Many2one(comodel_name="qms.finding")

    hazard_id = fields.Many2one(comodel_name="qms.hazard")

    goal_id = fields.Many2one(comodel_name="qms.goal")

    revision_by_direction_id = fields.Many2one(
        comodel_name="qms.revision_by_direction"
    )

    @api.model
    def create(self, vals):
        seq = self.env["ir.sequence"]
        vals["reference"] = seq.next_by_code("qms.action")
        action = super(Action, self).create(vals)
        return action

    @api.model
    def _stage_groups(self):
        stage_ids = self.env["qms.action.stage"].search([])
        return stage_ids

    @api.model
    def _get_stage_new(self):
        return self.env["qms.action.stage"].search([])

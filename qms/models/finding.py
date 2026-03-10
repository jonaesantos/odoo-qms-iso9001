# This model is based in some code used in OCA Management System Addons Project
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Finding(models.Model):

    _name = "qms.finding"
    _description = "Finding"
    _order = "create_date desc"

    @api.model
    def _default_stage(self):
        return self.env.ref("qms.finding_stage_draft", False) or self.env[
            "qms.finding.stage"
        ].search([("is_starting", "=", True)], limit=1)

    @api.model
    def _stage_groups(self, stages, domain):
        return self.env["qms.finding.stage"].search([])

    name = fields.Char(required=True)

    claimant_id = fields.Many2one(
        comodel_name="qms.interested_party", required=True, ondelete="restrict"
    )

    reference = fields.Char(required=True, readonly=True, default="NEW")

    closing_date = fields.Datetime(readonly=True)

    origin_ids = fields.Many2many(
        comodel_name="qms.finding.origin", required=True
    )

    stage_id = fields.Many2one(
        comodel_name="qms.finding.stage",
        copy=False,
        default=_default_stage,
        group_expand="_stage_groups",
        ondelete="restrict",
    )

    state = fields.Selection(related="stage_id.state", store=True)

    kanban_state = fields.Selection(
        selection=[
            ("normal", "In Progress"),
            ("done", "Ready For Next Stage"),
            ("blocked", "Blocked"),
        ],
        default="normal",
        required=True,
        copy=False,
    )

    action_ids = fields.Many2many(comodel_name="qms.action")

    description = fields.Html()

    interested_party_id = fields.Many2one(
        comodel_name="qms.interested_party", required=True, ondelete="restrict"
    )

    process_ids = fields.Many2many(comodel_name="qms.process", required=True)

    audit_ids = fields.Many2many(
        comodel_name="qms.audit", string="Related Audits"
    )

    def write(self, vals):
        # Reset kanban state on stage change
        is_state_change = "stage_id" in vals or "state" in vals
        if is_state_change:
            for finding in self:
                if finding.kanban_state != "normal":
                    vals["kanban_state"] = "normal"
                    break  # Only need to set it once for all records

        # Handle closing_date based on state change for each record
        if is_state_change and len(self) == 1:
            # Determine new state after the write
            new_stage = vals.get("stage_id")
            if new_stage:
                stage = self.env["qms.finding.stage"].browse(new_stage)
                new_state = stage.state
            else:
                new_state = vals.get("state")

            # Only modify closing_date if it needs to change
            if new_state == "done" and not self.closing_date:
                # Set closing date when closing
                vals["closing_date"] = fields.Datetime.now()
            elif new_state and new_state != "done" and self.closing_date:
                # Clear closing date when reopening (only if it was set)
                vals["closing_date"] = False

        return super(Finding, self).write(vals)

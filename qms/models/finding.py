# This model is based in some code used in OCA Management System Addons Project
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class Finding(models.Model):

    _name = "qms.finding"
    _description = "Finding"
    _order = "create_date desc"

    _kanban_states_ = [
        ("normal", _("In Progress")),
        ("done", _("Ready For Next Stage")),
        ("blocked", _("Blocked")),
    ]

    @api.model
    def _default_stage(self):
        return self.env.ref("qms.finding_stage_draft", False) or self.env[
            "qms.finding.stage"
        ].search([("is_starting", "=", True)], limit=1)

    @api.model
    def _stage_groups(self, stages, domain, order):
        return self.env["qms.finding.stage"].search([])

    name = fields.Char()

    claimant_id = fields.Many2one(
        comodel_name="qms.interested_party", required=True
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
    )

    state = fields.Selection(related="stage_id.state", store=True)

    kanban_state = fields.Selection(
        selection=_kanban_states_, default="normal", required=True, copy=False
    )

    action_ids = fields.Many2many(comodel_name="qms.action")

    description = fields.Html(required=True)

    interested_party_id = fields.Many2one(
        comodel_name="qms.interested_party", required=True
    )

    process_ids = fields.Many2many(comodel_name="qms.process", required=True)

    audit_ids = fields.Many2many(
        comodel_name="qms.audit", string="Related Audits"
    )

    def write(self, vals):
        is_writing = "is_writing" in self.env.context
        is_state_change = "stage_id" in vals or "state" in vals

        # Reset kanban state on stage change
        if is_state_change:
            for finding in self:
                if finding.kanban_state != "normal":
                    vals["kanban_state"] = "normal"
        result = super(Finding, self).write(vals)

        # Set/reset the closing date
        if not is_writing and is_state_change:
            for finding in self.with_context(is_writing=True):
                # On close set closing date
                if finding.state == "done" and not finding.closing_date:
                    finding.closing_date = fields.Datetime.now()
                # On reopen reset closing date
                if finding.state != "done" and finding.closing_date:
                    finding.closing_date = None
        return result

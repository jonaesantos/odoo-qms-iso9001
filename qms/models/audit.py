# This model is based in some code used in OCA Management System Addons Project
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class Audit(models.Model):

    _name = "qms.audit"
    _rec_name = "reference"
    _description = "Audit"

    system = fields.Selection(
        selection=[
            ("iso9001_2015", "ISO 9001:2015"),
            ("iso9001_2008", "ISO 9001:2008"),
        ],
        required=True,
    )

    reference = fields.Char(readonly=False, required=False)

    date = fields.Date()

    verification_line_ids = fields.One2many(
        comodel_name="qms.audit.verification.line", inverse_name="audit_id"
    )

    closing_date = fields.Datetime(readonly=True)

    strong_points = fields.Html()

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("open", "Open"),
            ("done", "Closed"),
        ],
        default="draft",
    )

    audited_ids = fields.Many2many(
        comodel_name="qms.interested_party", relation="audit_audited_rel"
    )

    auditors_ids = fields.Many2many(
        comodel_name="qms.interested_party", relation="audit_auditor_rel"
    )

    audit_evaluation_ids = fields.One2many(
        comodel_name="qms.audit.evaluation", inverse_name="audit_id"
    )

    non_conformity_ids = fields.One2many(
        comodel_name="qms.non_conformity", inverse_name="audit_id"
    )

    observation_ids = fields.One2many(
        comodel_name="qms.observation", inverse_name="audit_id"
    )

    opportunity_ids = fields.One2many(
        comodel_name="qms.opportunity", inverse_name="audit_id"
    )

    process_ids = fields.Many2many(comodel_name="qms.process", required=True)

    nc_count = fields.Integer(
        string="Non-Conformities",
        compute="_compute_finding_counts",
        store=True,
    )

    observation_count = fields.Integer(
        string="Observations",
        compute="_compute_finding_counts",
        store=True,
    )

    opportunity_count = fields.Integer(
        string="Opportunities",
        compute="_compute_finding_counts",
        store=True,
    )

    open_findings_count = fields.Integer(
        string="Open Findings",
        compute="_compute_finding_counts",
        store=True,
    )

    @api.depends(
        "non_conformity_ids",
        "observation_ids",
        "opportunity_ids",
        "non_conformity_ids.state",
        "observation_ids.state",
        "opportunity_ids.state",
    )
    def _compute_finding_counts(self):
        for audit in self:
            audit.nc_count = len(audit.non_conformity_ids)
            audit.observation_count = len(audit.observation_ids)
            audit.opportunity_count = len(audit.opportunity_ids)

            # Count open findings (not in 'done' or 'cancel')
            audit.open_findings_count = sum([
                len(audit.non_conformity_ids.filtered(
                    lambda x: x.state not in ("done", "cancel")
                )),
                len(audit.observation_ids.filtered(
                    lambda x: x.state not in ("done", "cancel")
                )),
                len(audit.opportunity_ids.filtered(
                    lambda x: x.state not in ("done", "cancel")
                )),
            ])

    def action_open(self):
        return self.write({"state": "open"})

    def button_close(self):
        return self.write(
            {"state": "done", "closing_date": fields.Datetime.now()}
        )

    @api.constrains("date", "closing_date")
    def _check_dates(self):
        for audit in self:
            if audit.closing_date and audit.date:
                closing_date_only = audit.closing_date.date()
                if closing_date_only < audit.date:
                    raise ValidationError(
                        _("Closing date cannot be earlier than audit date")
                    )

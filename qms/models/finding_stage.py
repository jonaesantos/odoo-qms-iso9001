from odoo import fields, models


class FindingStage(models.Model):

    _name = "qms.finding.stage"
    _description = "Finding Stage"
    _inherit = ["qms.stage"]

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("analysis", "Analysis"),
            ("pending", "Action Plan"),
            ("open", "In Progress"),
            ("done", "Closed"),
            ("cancel", "Cancelled"),
        ],
        readonly=True,
        default="draft",
    )

    fold = fields.Boolean()

from odoo import fields, models


class AuditEvaluation(models.Model):

    _name = "qms.audit.evaluation"
    _description = "Audit Evaluation"

    name = fields.Char(required=True)

    date = fields.Date()

    description = fields.Html()

    final_note = fields.Char()

    competent = fields.Char()

    responsible_id = fields.Many2one(
        comodel_name="qms.interested_party", required=True, ondelete="restrict"
    )

    type = fields.Selection(
        selection=[
            ("internal", "Internal"),
            ("external", "External"),
        ],
        string="System",
        required=False,
    )

    auditors_ids = fields.Many2many(
        comodel_name="qms.interested_party",
    )

    audit_id = fields.Many2one(comodel_name="qms.audit", ondelete="cascade")

    understanding = fields.Selection(
        selection=[
            ("-", "-"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
            ("5", "5"),
            ("6", "6"),
            ("7", "7"),
            ("8", "8"),
            ("9", "9"),
            ("10", "10"),
        ],
        default="-",
        required=False,
    )

    compliance = fields.Selection(
        selection=[
            ("-", "-"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
            ("5", "5"),
            ("6", "6"),
            ("7", "7"),
            ("8", "8"),
            ("9", "9"),
            ("10", "10"),
        ],
        default="-",
        required=False,
    )

    planning = fields.Selection(
        selection=[
            ("-", "-"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
            ("5", "5"),
            ("6", "6"),
            ("7", "7"),
            ("8", "8"),
            ("9", "9"),
            ("10", "10"),
        ],
        default="-",
        required=False,
    )

    report = fields.Selection(
        selection=[
            ("-", "-"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
            ("5", "5"),
            ("6", "6"),
            ("7", "7"),
            ("8", "8"),
            ("9", "9"),
            ("10", "10"),
        ],
        default="-",
        required=False,
    )

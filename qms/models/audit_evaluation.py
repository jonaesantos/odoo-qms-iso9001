from odoo import _, fields, models


class AuditEvaluation(models.Model):

    _name = "qms.audit.evaluation"
    _description = "Audit Evaluation"

    name = fields.Char()

    date = fields.Date()

    description = fields.Html()

    final_note = fields.Char()

    competent = fields.Char()

    responsible_id = fields.Many2one(
        comodel_name="qms.interested_party", required=True
    )

    _type_ = [("internal", _("Internal")), ("external", _("External"))]

    type = fields.Selection(selection=_type_, string="System", required=False)

    auditors_ids = fields.Many2many(
        comodel_name="qms.interested_party",
    )

    audit_id = fields.Many2one(comodel_name="qms.audit")

    _understanding_ = [
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
    ]

    understanding = fields.Selection(
        selection=_understanding_, default="-", required=False
    )

    _compliance_ = [
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
    ]

    compliance = fields.Selection(
        selection=_compliance_, default="-", required=False
    )

    _planning_ = [
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
    ]

    planning = fields.Selection(
        selection=_planning_, default="-", required=False
    )

    _report_ = [
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
    ]

    report = fields.Selection(selection=_report_, default="-", required=False)

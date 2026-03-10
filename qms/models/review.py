from odoo import fields, models


class Review(models.Model):

    _name = "qms.review"
    _description = "Review"

    name = fields.Char(required=True)

    date = fields.Date()

    conclusion = fields.Html()

    policy_id = fields.Many2one(comodel_name="qms.policy", ondelete="cascade")

    document_id = fields.Many2one(comodel_name="qms.document", ondelete="cascade")

    procedure_id = fields.Many2one(comodel_name="qms.procedure", ondelete="cascade")

    instructive_id = fields.Many2one(comodel_name="qms.instructive", ondelete="cascade")

    registry_id = fields.Many2one(comodel_name="qms.registry", ondelete="cascade")

    goal_id = fields.Many2one(comodel_name="qms.goal", ondelete="cascade")

    process_id = fields.Many2one(comodel_name="qms.process", ondelete="cascade")

    hazard_id = fields.Many2one(comodel_name="qms.hazard", ondelete="cascade")

    indicator_id = fields.Many2one(comodel_name="qms.indicator", ondelete="cascade")

    responsible_id = fields.Many2one(
        comodel_name="qms.interested_party", required=True, ondelete="restrict"
    )

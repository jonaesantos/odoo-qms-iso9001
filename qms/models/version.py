from odoo import fields, models


class Version(models.Model):

    _name = "qms.version"
    _description = "Version"

    version = fields.Char()

    change_history = fields.Html()

    date_open = fields.Date()

    document_id = fields.Many2one(
        comodel_name="qms.document", ondelete="cascade"
    )

    policy_id = fields.Many2one(comodel_name="qms.policy", ondelete="cascade")

    indicator_id = fields.Many2one(
        comodel_name="qms.indicator", ondelete="cascade"
    )

    procedure_id = fields.Many2one(
        comodel_name="qms.procedure", ondelete="cascade"
    )

    instructive_id = fields.Many2one(
        comodel_name="qms.instructive", ondelete="cascade"
    )

    registry_id = fields.Many2one(
        comodel_name="qms.registry", ondelete="cascade"
    )

    responsible_id = fields.Many2one(
        comodel_name="qms.interested_party", required=True
    )

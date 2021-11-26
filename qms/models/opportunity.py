from odoo import api, fields, models


class Opportunity(models.Model):

    _name = "qms.opportunity"
    _description = "Opportunity"
    _inherit = ["qms.finding"]

    action_ids = fields.One2many(
        comodel_name="qms.action", inverse_name="opportunity_id"
    )

    audit_id = fields.Many2one(comodel_name="qms.audit")

    revision_by_direction_id = fields.Many2one(
        comodel_name="qms.revision_by_direction"
    )

    indicator_id = fields.Many2one(comodel_name="qms.indicator")

    @api.model
    def create(self, vals):
        vals.update(
            {
                "reference": self.env["ir.sequence"].next_by_code(
                    "qms.opportunity"
                )
            }
        )
        return super(Opportunity, self).create(vals)

from odoo import api, fields, models


class Opportunity(models.Model):

    _name = "qms.opportunity"
    _description = "Opportunity"
    _inherit = ["qms.finding"]

    action_ids = fields.One2many(
        comodel_name="qms.action", inverse_name="opportunity_id"
    )

    audit_id = fields.Many2one(comodel_name="qms.audit", ondelete="set null")

    revision_by_direction_id = fields.Many2one(
        comodel_name="qms.revision_by_direction", ondelete="set null"
    )

    indicator_id = fields.Many2one(comodel_name="qms.indicator", ondelete="set null")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals.update(
                {
                    "reference": self.env["ir.sequence"].next_by_code(
                        "qms.opportunity"
                    )
                }
            )
        return super(Opportunity, self).create(vals_list)

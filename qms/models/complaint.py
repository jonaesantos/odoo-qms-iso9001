from odoo import api, fields, models


class Complaint(models.Model):

    _name = "qms.complaint"
    _description = "Complaint"
    _inherit = ["qms.finding", "qms.weakness"]

    action_ids = fields.One2many(
        comodel_name="qms.action", inverse_name="complaint_id"
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals.update(
                {
                    "reference": self.env["ir.sequence"].next_by_code(
                        "qms.complaint"
                    )
                }
            )
        return super(Complaint, self).create(vals_list)

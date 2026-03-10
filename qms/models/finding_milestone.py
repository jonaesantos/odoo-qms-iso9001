from odoo import api, fields, models


class FindingMilestone(models.Model):

    _name = "qms.finding.milestone"
    _description = "Finding Milestone"
    _order = "sequence"

    name = fields.Char(required=True, translate=True)

    description = fields.Text()

    sequence = fields.Integer()

    parent_path = fields.Char(index=True)

    reference_code = fields.Char()

    @api.depends("name")
    def _compute_display_name(self):
        for obj in self:
            obj.display_name = obj.name

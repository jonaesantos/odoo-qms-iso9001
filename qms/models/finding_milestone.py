from odoo import fields, models


class FindingMilestone(models.Model):

    _name = "qms.finding.milestone"
    _description = "Finding Milestone"
    _order = "sequence"

    name = fields.Char(required=True, translate=True)

    description = fields.Text()

    sequence = fields.Integer()

    parent_path = fields.Char(index=True)

    reference_code = fields.Char()

    def name_get(self):
        res = []
        for obj in self:
            name = obj.name
            if obj.parent_id:
                name = obj.parent_id.name_get()[0][1] + " / " + name
            res.append((obj.id, name))
        return res

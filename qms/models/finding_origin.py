from odoo import _, api, exceptions, fields, models


class FindingOrigin(models.Model):

    _name = "qms.finding.origin"
    _order = "parent_id, sequence"
    _parent_store = True
    _inherit = ["qms.finding.milestone"]

    parent_id = fields.Many2one(
        comodel_name="qms.finding.origin", string="Group", ondelete="restrict"
    )

    child_ids = fields.One2many(
        comodel_name="qms.finding.origin",
        inverse_name="parent_id",
        string="Child origins",
    )

    @api.constrains("parent_id")
    def _check_recursion(self):
        if not super(FindingOrigin, self)._check_recursion():
            raise exceptions.ValidationError(
                _("Error! Cannot create recursive cycle.")
            )
        return

from odoo import _, api, exceptions, fields, models


class WeaknessCause(models.Model):

    _name = "qms.weakness.cause"
    _description = "Weakness Cause"
    _order = "parent_id, sequence"
    _parent_store = True
    _inherit = ["qms.finding.milestone"]

    parent_id = fields.Many2one(
        comodel_name="qms.weakness.cause", string="Group", ondelete="restrict"
    )

    child_ids = fields.One2many(
        comodel_name="qms.weakness.cause",
        inverse_name="parent_id",
        string="Child Causes",
    )

    @api.constrains("parent_id")
    def _check_recursion(self):
        if not super(WeaknessCause, self)._check_recursion():
            raise exceptions.ValidationError(
                _("Error! Cannot create recursive cycle.")
            )
        return

# This model is based in some code used in OCA Management System Addons Project
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models


class GoalMeasurement(models.Model):

    _name = "qms.goal.measurement"
    _description = "Goal Measurement"

    name = fields.Char(string="Measurement", required=True)

    goal = fields.Char()

    goal_id = fields.Many2one(
        comodel_name="qms.goal", ondelete="cascade", string="Goals"
    )

    expected_date = fields.Date()

    measurement_date = fields.Date()

    comments = fields.Text()

    _result_ = [
        ("goal_ok", _("Goal achieved")),
        ("goal_with_obs", _("Goal achieved with comments")),
        ("goal_no_ok", _("Goal not achieved")),
    ]

    result = fields.Selection(selection=_result_, required=False)

    result_detail = fields.Char()

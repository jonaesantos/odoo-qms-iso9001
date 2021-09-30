# This model is based in some code used in OCA Management System Addons Project
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models


class GoalMeasurement(models.Model):

    _name = "qms.goal.measurement"

    name = fields.Char(string="Measurement", required=True)

    goal = fields.Char()

    goal_id = fields.Many2one(comodel_name="qms.goal", ondelete="cascade")

    expected_date = fields.Date()

    measurement_date = fields.Date()

    comments = fields.Text()

    _result_ = [
        ("goal_ok", _("Meta alcanzada")),
        ("goal_with_obs", _("Meta alcanzada con observaciones")),
        ("goal_no_ok", _("Meta no alzanzada")),
    ]

    result = fields.Selection(selection=_result_, required=False)

    result_detail = fields.Char()

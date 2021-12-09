# This model is based in some code used in OCA Management System Addons Project
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models


class IndicatorMeasurement(models.Model):

    _name = "qms.indicator.measurement"
    _description = "Indicator Measurement"

    name = fields.Char(string="Measurement", required=True)

    goal = fields.Char()

    indicator_id = fields.Many2one(
        comodel_name="qms.indicator", ondelete="cascade"
    )

    expected_date = fields.Date()

    measurement_date = fields.Date()

    comments = fields.Text()

    _result_ = [
        ("goal_ok", _("Goal reached")),
        ("goal_with_obs", _("Goal reached with observations")),
        ("goal_no_ok", _("Unachieved target")),
    ]

    result = fields.Selection(selection=_result_, required=False, store=True)

    result_detail = fields.Char()

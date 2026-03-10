from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Goal(models.Model):

    _name = "qms.goal"
    _description = "Goal"

    name = fields.Char(required=True)

    description = fields.Html()

    cancel_date = fields.Date(readonly=True)

    date_open = fields.Datetime()

    date_close = fields.Datetime()

    approved = fields.Boolean()

    responsible_id = fields.Many2one(
        comodel_name="qms.interested_party", required=True, ondelete="restrict"
    )

    process_ids = fields.Many2many(comodel_name="qms.process", required=True)

    resource_ids = fields.Many2many(comodel_name="qms.resource")

    measurement_ids = fields.One2many(
        comodel_name="qms.goal.measurement", inverse_name="goal_id"
    )

    action_ids = fields.One2many(
        comodel_name="qms.action", inverse_name="goal_id"
    )

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("open", "Open"),
            ("closed", "Closed"),
            ("cancelled", "Cancelled"),
        ],
        default="draft",
        required=True,
    )

    review_ids = fields.One2many(
        comodel_name="qms.review", inverse_name="goal_id"
    )

    last_measurement_date = fields.Date(
        compute="_compute_last_measurement_date", store=True
    )

    last_measurement_result = fields.Char(
        compute="_compute_last_measurement_result", store=True
    )

    last_review_date = fields.Date(compute="_compute_last_review_date", store=True)

    action_count = fields.Integer(
        string="Actions",
        compute="_compute_action_count",
        store=True,
    )

    @api.depends("measurement_ids.measurement_date")
    def _compute_last_measurement_date(self):
        for goal in self:
            if goal.measurement_ids:
                last_measurement = goal.measurement_ids.sorted(
                    key=lambda r: r.measurement_date, reverse=True
                )
                goal.last_measurement_date = last_measurement[0].measurement_date
            else:
                goal.last_measurement_date = False

    @api.depends("measurement_ids.measurement_date", "measurement_ids.result")
    def _compute_last_measurement_result(self):
        for goal in self:
            if goal.measurement_ids:
                last_measurement = goal.measurement_ids.sorted(
                    key=lambda r: r.measurement_date, reverse=True
                )
                goal.last_measurement_result = last_measurement[0].result
            else:
                goal.last_measurement_result = False

    @api.depends("review_ids.date")
    def _compute_last_review_date(self):
        for goal in self:
            if goal.review_ids:
                last_review = goal.review_ids.sorted(
                    key=lambda r: r.date, reverse=True
                )
                goal.last_review_date = last_review[0].date
            else:
                goal.last_review_date = False

    @api.depends("action_ids")
    def _compute_action_count(self):
        for goal in self:
            goal.action_count = len(goal.action_ids)

    def write(self, vals):
        # Handle automatic date setting when state changes via statusbar
        if "state" in vals:
            new_state = vals["state"]

            # Set date_open when opening (if not already set)
            if new_state == "open":
                for goal in self:
                    if not goal.date_open:
                        vals["date_open"] = fields.Datetime.now()
                        break

            # Set date_close when closing (if not already set)
            elif new_state == "closed":
                for goal in self:
                    if not goal.date_close:
                        vals["date_close"] = fields.Datetime.now()
                        break

            # Set cancel_date when cancelling (if not already set)
            elif new_state == "cancelled":
                for goal in self:
                    if not goal.cancel_date:
                        vals["cancel_date"] = fields.Date.today()
                        break

        return super(Goal, self).write(vals)

    def action_toggle_approved(self):
        self.approved = not self.approved

    def action_draft(self):
        self.state = "draft"

    def action_open(self):
        self.state = "open"
        if not self.date_open:
            self.date_open = fields.Datetime.now()

    def action_close(self):
        self.state = "closed"
        if not self.date_close:
            self.date_close = fields.Datetime.now()

    def action_cancel(self):
        self.state = "cancelled"
        if not self.cancel_date:
            self.cancel_date = fields.Date.today()

    @api.constrains("date_open", "date_close")
    def _check_dates(self):
        for goal in self:
            if goal.date_close and goal.date_open:
                if goal.date_close < goal.date_open:
                    raise ValidationError(
                        _("Close date must be after open date")
                    )

    @api.constrains("state", "date_open")
    def _check_open_date_required(self):
        for goal in self:
            if goal.state in ("open", "closed") and not goal.date_open:
                raise ValidationError(
                    _("Opening date is required when goal is in Open or Closed state")
                )

    @api.constrains("state", "date_close")
    def _check_close_date_required(self):
        for goal in self:
            if goal.state == "closed" and not goal.date_close:
                raise ValidationError(
                    _("Closing date is required when goal is in Closed state")
                )

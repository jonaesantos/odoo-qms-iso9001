# -*- coding: utf-8 -*-
# This model is based in some code used in OCA Management System Addons Project
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class Finding(models.Model):

    _name = 'qms.finding'
    _order = 'create_date desc'
    _rec_name = 'description'

    _kanban_states_ = [
        ('normal', 'In Progress'),
        ('done', 'Ready For Next Stage'),
        ('blocked', 'Blocked')
    ]

    @api.model
    def _default_stage(self):
        return (
            self.env.ref('qms.finding_stage_draft', False) or
            self.env['qms.finding.stage'].search(
                [('is_starting', '=', True)],
                limit=1
            )
        )

    @api.model
    def _stage_groups(self, stages, domain, order):
        return self.env['qms.finding.stage'].search([])

    name = fields.Char()

    reference = fields.Char(
        required=True,
        readonly=True,
        default='NEW'
    )

    closing_date = fields.Datetime(
        readonly=True
    )

    origin_ids = fields.Many2many(
        comodel_name='qms.finding.origin',
        required=True
    )

    stage_id = fields.Many2one(
        comodel_name='qms.finding.stage',
        copy=False,
        default=_default_stage,
        group_expand='_stage_groups'
    )

    state = fields.Selection(
        related='stage_id.state',
        store=True
    )

    kanban_state = fields.Selection(
        selection=_kanban_states_,
        default='normal',
        required=True,
        copy=False
    )

    action_ids = fields.Many2many(
        comodel_name='qms.action'
    )

    action_plan_comments = fields.Text()

    evaluation_comments = fields.Text()

    description = fields.Text(
        required=True
    )

    interested_party_id = fields.Many2one(
        comodel_name='qms.interested_party',
        required=True
    )

    process_ids = fields.Many2many(
        comodel_name='qms.process',
        required=True
    )

    audit_ids = fields.Many2many(
        comodel_name='qms.audit',
        string='Related Audits'
    )

    @api.multi
    def _get_all_actions(self):
        self.ensure_one()
        return (self.action_ids + self.immediate_action_id)

    @api.constrains('stage_id')
    def _check_open_with_action_comments(self):
        for finding in self:
            if finding.state == 'open' and not finding.action_plan_comments:
                raise models.ValidationError(
                    _("Action plan comments are required \
                      in order to put a finding 'In Progress'.")
                )

    @api.constrains('stage_id')
    def _check_close_with_evaluation(self):
        for finding in self:
            if finding.state == 'done':
                if not finding.evaluation_comments:
                    raise models.ValidationError(
                        _("Evaluation Comments are required \
                          in order to close a finding.")
                    )
                actions_are_closed = (
                    action.stage_id.is_ending
                    for action in finding._get_all_actions())
                if not all(actions_are_closed):
                    raise models.ValidationError(
                        _("All actions must be done \
                          before closing a finding.")
                    )

    @api.multi
    def write(self, vals):
        is_writing = 'is_writing' in self.env.context
        is_state_change = 'stage_id' in vals or 'state' in vals

        # Reset kanban state on stage change
        if is_state_change:
            was_not_open = {
                x.id: x.state in ('draft',
                                  'analysis', 'pending') for x in self}
            for finding in self:
                if finding.kanban_state != 'normal':
                    vals['kanban_state'] = 'normal'

        result = super(Finding, self).write(vals)

        # Set/reset the closing date
        if not is_writing and is_state_change:
            for finding in self.with_context(is_writing=True):
                # On close set closing date
                if finding.state == 'done' and not finding.closing_date:
                    finding.closing_date = fields.Datetime.now()
                # On reopen reset closing date
                if finding.state != 'done' and finding.closing_date:
                    finding.closing_date = None
                # On action plan approval open the actions
                if finding.state == 'open' and was_not_open[finding.id]:
                    for action in finding._get_all_actions():
                        if action.stage_id.is_starting:
                            action.case_open()
        return result

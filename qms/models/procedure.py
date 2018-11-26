# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class Procedure(models.Model):

    _name = "qms.procedure"
    _inherit = ['qms.document']
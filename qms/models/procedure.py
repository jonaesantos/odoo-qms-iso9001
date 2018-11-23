# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class Procedure(models.Model):

    _name = "qms.document.procedure"

    name = fields.Char(
        required=True
    )

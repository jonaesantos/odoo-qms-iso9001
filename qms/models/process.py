# -*- coding: utf-8 -*-

from odoo import fields, models


class Process(models.Model):

    _name = "qms.process"

    name = fields.Char(
        required=True
    )

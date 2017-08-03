# -*- coding: utf-8 -*-

from odoo import fields, models


class Resource(models.Model):

    _name = "qms.resource"

    name = fields.Char()

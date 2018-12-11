# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class Registry(models.Model):

    _name = "qms.registry"
    _inherit = 'qms.document'

    name = fields.Char(
        required=True
    )

    version_ids = fields.One2many(
        comodel_name='qms.version',
        inverse_name='registry_id'
    )
    
     
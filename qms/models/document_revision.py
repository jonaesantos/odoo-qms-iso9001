# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class Document_Revision(models.Model):

    _name = "qms.document.revision"

    revision = fields.Char()

    comments = fields.Html()

    date_open = fields.Date()

    _state_ = [
        ('draft', 'Draft'),        
        ('valid', 'Valid'),
        ('obsolete', 'Obsolete')
    ]

    state = fields.Selection(
        selection=_state_,
        default='valid',
        required=False
    )

    document_id = fields.Many2one(
        comodel_name='qms.document',
        ondelete='cascade'
    )    

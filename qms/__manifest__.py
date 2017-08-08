# -*- coding: utf-8 -*-

{
    'name': "QMS",
    'summary': 'ISO 9001 Quality Management System',
    'description': '''
        Odoo addon for ISO 9001 Quality Management System. Based on some \
        models developed by Odoo Community Association for management systems \
        available at https://github.com/OCA/management-system/
        ''',
    'website': 'https://www.tmcrosario.gob.ar',
    'version': '10.0.1.0.0',
    'author': 'TMC Rosario, Odoo Community Association',
    'license': 'AGPL-3',
    'sequence': 150,
    'depends': [],
    'data': [
        # 'security/groups.xml',
        # 'security/ir.model.access.csv',
        'data/action_sequence.xml',
        'data/action_stage.xml',
        'views/policy.xml',
        'views/interested_party.xml',
        'views/resource.xml',
        'views/goal.xml',
        'views/hazard.xml',
        'views/action.xml',
        'views/action_stage.xml',
        'views/menu.xml'
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'qweb': [],
}

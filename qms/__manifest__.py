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
        'data/audit_sequence.xml',
        'data/non_conformity_sequence.xml',
        'data/opportunity_sequence.xml',
        'data/action_stage.xml',
        'data/weakness_cause.xml',
        'data/finding_origin.xml',
        'data/finding_stage.xml',
        'views/policy.xml',
        'views/review.xml',
        'views/interested_party.xml',
        'views/resource.xml',
        'views/goal.xml',
        'views/hazard.xml',
        'views/effectiveness_check.xml',
        'views/action.xml',
        'views/action_stage.xml',
        'views/audit.xml',
        'views/audit_verification_line.xml',
        'views/finding_milestone.xml',
        'views/weakness_cause.xml',
        'views/finding_origin.xml',
        'views/finding_stage.xml',
        'views/finding.xml',
        'views/non_conformity.xml',
        'views/opportunity.xml',
        'views/menu.xml'
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'qweb': [],
}

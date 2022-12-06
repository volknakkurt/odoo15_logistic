# -*- coding: utf-8 -*-

{
    'name': 'Hospital Management',
    'version': '1.0.0',
    'category': 'Hospital',
    'author': 'Volkan',
    'sequence': -100,
    'summary': 'Hospital management system',
    'description': "Hospital management system controller",
    'depends': [
        'mail',
        'hr',
        'product',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/cancel_appointment_view.xml',
        'views/menu.xml',
        'views/patient_view.xml',
        'views/appointment_view.xml',
        'views/patient_tag_view.xml',
        'views/male.patient.view.xml',
        'views/female.patient.view.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'assets': {},
    'license': 'LGPL-3'
}

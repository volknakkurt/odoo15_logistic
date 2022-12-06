# -*- coding: utf-8 -*-

{
    'name': 'Logistic Management',
    'version': '1.0.0',
    'category': 'Logistic',
    'author': 'Volkan',
    'sequence': -110,
    'summary': 'Logistic management system',
    'description': "Logistic management system controller",
    'depends': [
        'mail',
        'hr',
        'account',
        'fleet',
        'product',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/cargo_management_view.xml',
        'views/menu.xml',
        'views/cargo_information_view.xml',
        'wizard/cargo_management_view.xml',
        'views/customer_view.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'assets': {},
    'license': 'LGPL-3'
}

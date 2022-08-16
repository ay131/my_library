# -*- coding: utf-8 -*-
{
    'name': "my_library",

    'summary': "",

    'description': "",

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'application': True,
    'auto_install': False,

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'views/library_book.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

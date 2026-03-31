# -*- coding: utf-8 -*-
{
    'name': "crm_extend",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
    Specific module made for customs' information.
    """,

    'author': "Enish",
    'website': "https://github.com/Enikish",


    'category': 'Service',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/templates.xml',
        'wizard/customer_import_wizard_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': False
}


# -*- coding: utf-8 -*-
{
    'name': "card_extend",

    'summary': "Storage extend for Mary And Mouse Wizard Card Store",

    'description': """
    This module includes storage and sale extend for Mary And Mouse Wizard Card, 
    like scrapping information from website and saving in database.
    """,

    'author': "Enish/Enikish",

    'category': 'Mary And Mouse',
    'version': '0.1',

    'depends': ['base', 'product'],

    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/views.xml',
    ],
    'installable': True,
    'application': False,
}


# -*- coding: utf-8 -*-
{
    'name': "sm_carsharing_structure_sommobilitat",

    'summary': """
         Extra fields any enterprise would need to add to fleet vehicle""",

    'author': "Som Mobilitat",
    'website': "https://www.sommobilitat.coop",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': '',
    'version': '11.0.0.0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','vertical_carsharing','fleet','sm_carsharing_structure'],

    # always loaded
    'data': [
        'views/views_cs_car.xml'
    ],
}

# -*- coding: utf-8 -*-
{
  'name': "sm_reports",

  'summary': """
    reporting engine for carsgharing system
  """,

  'author': "Som Mobilitat",
  'website': "https://www.sommobilitat.coop",

  # Categories can be used to filter modules in modules listing
  # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
  # for the full list
  'category': 'Uncategorized',
  'version': '11.0.0.0.2',

  # any module necessary for this one to work correctly
  'depends': ['base'],

  # always loaded
  'data': [
    'views/default_template.xml',
    'views/views_members.xml'
  ],
  # only loaded in demonstration mode
  'demo': [],
}

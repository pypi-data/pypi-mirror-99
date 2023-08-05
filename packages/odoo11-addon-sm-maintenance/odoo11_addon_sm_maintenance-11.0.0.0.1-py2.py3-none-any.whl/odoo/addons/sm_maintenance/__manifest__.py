# -*- coding: utf-8 -*-
{
  'name': "sm_maintenance",

  'summary': """
    Module containing a set of sm_maintenance tasks to be executed periodically
    and keep database entries and sm services healthy""",

  'description': """
    Module containing a set of sm_maintenance tasks to be executed periodically
    and keep database entries and sm services healthy
  """,

  'author': "Som Mobilitat",
  'website': "https://www.sommobilitat.coop",

  # Categories can be used to filter modules in modules listing
  # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
  # for the full list
  'category': 'Mobility',
  'version': '11.0.0.0.1',

  # any module necessary for this one to work correctly
  'depends': ['base', 'account', 'sm_connect'],

  # always loaded
  'data': [
    'security/ir.model.access.csv',
    'views/views_successful_action_message.xml',
  ],
  # only loaded in demonstration mode
  'demo': [],
}

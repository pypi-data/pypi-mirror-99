# -*- coding: utf-8 -*-
{
  'name': "sm_collaborators",

  'summary': """""",

  'description': """""",

  'author': "Som Mobilitat",
  'website': "http://www.sommobilitat.coop",

  # Categories can be used to filter modules in modules listing
  # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
  # for the full list
  'category': 'Mobility',
  'version': '11.0.0.0.3',

  # any module necessary for this one to work correctly
  'depends': ['base','vertical_carsharing'],

  # always loaded
  'data': [
    'security/ir.model.access.csv',
    'views/views.xml',
    'views/views_collaborator.xml',
    'views/views_collaborator_actions.xml',
    'views/views_collaborator_fetch_wizard.xml',
  ],
  # only loaded in demonstration mode
  'demo': [],
}

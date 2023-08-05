# -*- coding: utf-8 -*-
{
  'name': "carsharing_structure",

  'summary': """
    This module will organice everything that needs to be done in a car and a parking as projects. Also to define account structure for cs service""",

  'author': "Som Mobilitat",
  'website': "https://www.sommobilitat.coop",

  # Categories can be used to filter modules in modules listing
  # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
  # for the full list
  'category': 'carsharing',
  'version': '11.0.0.0.2',

  # any module necessary for this one to work correctly
  'depends': ['base','vertical_carsharing','project','fleet','sm_partago_db'],

  # always loaded
  'data': [
    'security/ir.model.access.csv',
    'views/views.xml',
    'views/views_cs_car.xml',
    'views/views_cs_car_service.xml',
    'views/views_cs_carconfig.xml',
    'views/views_cs_production_unit.xml',
    'views/views_cs_community.xml',
    'views/views_cs_task.xml',
    'views/views_cs_task_wizard.xml'
  ],
  # only loaded in demonstration mode
  'demo': [
    #'demo/demo.xml',
  ],
}

{
  'name': "sm_partago_accounting",

  'summary': """
    Module to manage app accounting integrated in odoo
  """,

  'author': "Som Mobilitat",
  'website': "https://www.sommobilitat.coop",

  # Categories can be used to filter modules in modules listing
  # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
  # for the full list
  'category': 'Uncategorized',
  'version': '11.0.0.0.2',

  # any module necessary for this one to work correctly
  'depends': ['base','vertical_carsharing','sm_partago_db','sm_partago_user'],

  # always loaded
  'data': [
    'views/views_members.xml'
  ],
  # only loaded in demonstration mode
  'demo': [],
}

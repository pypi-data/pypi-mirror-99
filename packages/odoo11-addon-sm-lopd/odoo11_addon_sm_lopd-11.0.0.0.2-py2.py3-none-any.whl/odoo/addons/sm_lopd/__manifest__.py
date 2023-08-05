# -*- coding: utf-8 -*-
{
  'name': "sm_lopd",

  'summary': """
  Manage GDPR contract send
  """,

  'author': "Som Mobilitat",
  'website': "https://www.sommobilitat.coop",

  # Categories can be used to filter modules in modules listing
  # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
  # for the full list
  'category': 'carsharing',
  'version': '11.0.0.0.2',

  # any module necessary for this one to work correctly
  'depends': ['base','sm_partago_user'],

  # always loaded
  'data': [
    # 'security/ir.model.access.csv'
    'report/lopd_report.xml',
    'email_tmpl/lopd_email.xml',
    'email_tmpl/lopd_companies_template.xml',
    'views/views_cron.xml',
    'views/views_res_config_settings.xml',
    'views/views_members.xml',
  ],
  # only loaded in demonstration mode
  'demo': [],
}

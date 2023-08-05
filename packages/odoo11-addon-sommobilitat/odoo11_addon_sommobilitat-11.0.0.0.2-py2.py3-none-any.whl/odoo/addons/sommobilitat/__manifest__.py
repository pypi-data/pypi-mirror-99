# -*- coding: utf-8 -*-
{
  'name': "sommobilitat",

  'summary': """Som Mobilitat crm / erp""",

  'author': "Som Mobilitat",
  'website': "http://www.sommobilitat.coop",

  'category': 'Mobility',
  'version': '11.0.0.0.2',

  'depends': ['base','vertical_carsharing'],

  'data': [
    #'security/sommobilitat_security.xml',
    'security/ir.model.access.csv',
    'views/views.xml',
    'views/views_members.xml',
    'views/views_members_actions.xml',
    'views/views_members_fetch_wizard.xml',
    'views/views_cron.xml'
  ],
}

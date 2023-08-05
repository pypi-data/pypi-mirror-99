# -*- coding: utf-8 -*-
{
  'name': "sm_member_geolocation",

  'summary': """
    Locate your members and calculate zones""",

  'author': "Som Mobilitat",
  'website': "https://www.sommobilitat.coop",

  'category': 'mobility',
  'version': '11.0.0.0.2',

  'depends': ['base','base_geolocalize'],

  'data': [
    'security/ir.model.access.csv',
    'views/views_cron.xml',
    'views/views_members.xml',
    'views/views_members_zone.xml'
  ],
  'demo': []
}

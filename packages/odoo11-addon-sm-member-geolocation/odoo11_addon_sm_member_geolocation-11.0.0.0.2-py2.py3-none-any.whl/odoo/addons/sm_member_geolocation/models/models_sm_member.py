# -*- coding: utf-8 -*-
import json
import requests

from odoo import models, fields, api
from odoo.tools.translate import _

from odoo.addons.sm_maintenance.models.models_load_data import load_data

class sm_member(models.Model):
  _inherit = 'res.partner'
  _name = 'res.partner'

  _company_data = load_data.get_instance()

  geolocation_computed = fields.Boolean(string=_("Geolocation done"))
  computed_city = fields.Char(string=_("City (computed)"))
  computed_state = fields.Char(string=_("State (computed)"))
  computed_country = fields.Char(string=_("Country (computed)"))
  member_lat = fields.Float(string=_("Lat (computed)"), digits=(16, 16))
  member_lng = fields.Float(string=_("Lng (computed)"), digits=(16, 16))
  partner_zones = fields.Many2many('sm_member_geolocation.members_zone', 
    'sm_geolocation_partners_zone', 'partner_id', 'zone_id',string=_("Related zones"))
  # city_computed_manually_modified = fields.Boolean(string=_("City (Computed) manually modified"))

  API_KEY = _company_data.zip_api_info()['api_key']
  END_POINT = 'https://maps.googleapis.com/maps/api/geocode/json?'

  @api.constrains('computed_city')
  def check_lat_lng(self, request=None, member=None):
    if request is None and member is None:
      if self.computed_city:
        request = self.END_POINT \
          + 'address=' \
          + self.computed_city \
          + '&' 'components=country:ES&key=' \
          + self.API_KEY
        req = requests.get(request)

        if req.status_code == 200:
          json_data = json.loads(req.text)
          results = json_data['results']
          for result in results:
            self.calculate_lat_lng(result)
    else:
      for result in request:
        self.calculate_lat_lng(result, member)

  def calculate_lat_lng(self, result, member=None):
    location = (result['geometry']['location'])

    if member is None:
      self.write({'member_lat': location['lat'],
        'member_lng': location['lng']})
    else:
      member.write({'member_lat': location['lat'],
        'member_lng': location['lng']})

  # TODO: cron to compute this
  # self.compute_api_address()

  @api.model
  def compute_api_address_from_action(self):
    if self.env.context:
      if 'active_ids' in self.env.context:
        members = self.env['res.partner'].browse(self.env.context['active_ids'])
        if members.exists():
          for member in members:
            member.compute_api_address()

    return self._resources.get_successful_action_message(self,
      _('Compute api address done successfully'), self._name)

  def compute_api_address(self):
    if self.zip:
      request = self.END_POINT + 'address=&' \
        'components=' \
        'country:ES|' \
        'postal_code:' + self.zip + '&key=' + self.API_KEY

      req = requests.get(request)
      if req.status_code == 200:
        json_data = json.loads(req.text)
        results = json_data['results']
        self.check_lat_lng(results, self)

        for result in results:
          city = ""
          state = ""
          country = ""

          if 'address_components' in result:
            data = result['address_components']

            for index in range(0, len(data) - 1):
              address_type = data[index]['types'][0]

              if address_type == 'locality':
                city = data[index]['long_name']

              elif address_type == 'administrative_area_level_2':
                state = data[index]['long_name']

              elif address_type == 'country':
                country = data[index]['long_name']

          self.write({
            'computed_city': city,
            'computed_state': state,
            'computed_country': country
          })
    self.write({'geolocation_computed': True})


  computed_city = fields.Char(string=_("City (computed)"))
  computed_state = fields.Char(string=_("State (computed)"))
  computed_country = fields.Char(string=_("Country (computed)"))
  member_lat = fields.Float(string=_("Lat (computed)"), digits=(16, 16))
  member_lng = fields.Float(string=_("Lng (computed)"), digits=(16, 16))

  @api.model
  def sanitize_geolocation_db_action(self):
    if self.env.context:
      if 'active_ids' in self.env.context:
        members = self.env['res.partner'].browse(self.env.context['active_ids'])
        if members.exists():
          for member in members:
            if member.computed_state or member.computed_city or member.member_lat or member.member_lng:
              print("GEOLOCATION COMPUTED")
              member.write({'geolocation_computed': True})

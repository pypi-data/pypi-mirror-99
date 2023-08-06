# -*- coding: utf-8 -*-

from math import radians, cos, sin, asin, sqrt

from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.addons.sm_maintenance.models.models_sm_utils import sm_utils
from odoo.addons.sm_maintenance.models.models_sm_resources import sm_resources


def calculate_distance_between_two_points(lon1, lat1, lon2, lat2):
  lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

  dlon = lon2 - lon1
  dlat = lat2 - lat1
  a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
  c = 2 * asin(sqrt(a))
  r = 6371  # Radius of earth in kilometers
  return c * r


class sm_members_zone(models.TransientModel):
  _name = "sm_member_geolocation.members_zone"

  name = fields.Char(string=_('Name'))
  lat = fields.Float(string=_('Lat'), digits=(16, 16))
  lng = fields.Float(string=_('Lng'), digits=(16, 16))
  rad = fields.Integer(string=_('Rad (Km)'))

  zone_partners = fields.Many2many('res.partner', 'sm_geolocation_partners_zone', 'zone_id', 'partner_id',
    string=_("Members"), copy=False)

  @api.multi
  def search_members_inside_action(self):
    if self.env.context:
      if 'active_ids' in self.env.context:
        computes = self.env['sm_member_geolocation.members_zone'].browse(self.env.context['active_ids'])
        if computes.exists():
          for compute in computes:
            members = self.env['res.partner'].sudo().search([])
            if members.exists():
              lat = compute.lat
              lng = compute.lng
              for member in members:
                result = calculate_distance_between_two_points(
                  lng, lat, member.member_lng, member.member_lat)
                if result <= compute.rad:
                  compute.zone_partners = [(4, member.id)]

    return sm_resources.getInstance().get_successful_action_message(self,
      _('Search members inside done successfully'), self._name)

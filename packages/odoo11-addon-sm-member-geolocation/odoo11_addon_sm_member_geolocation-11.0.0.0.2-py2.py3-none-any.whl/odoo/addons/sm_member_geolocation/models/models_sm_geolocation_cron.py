from odoo import models, api
from odoo.tools.translate import _
from odoo.addons.sm_maintenance.models.models_sm_utils import sm_utils


class sm_geolocation_cron(models.Model):
  _name = 'sm_member_geolocation.sm_geolocation_cron'

  @api.model
  def geolocate_cron(self):
    members = self.env['res.partner'].search([('geolocation_computed','=',False)])
    if members.exists():
      for member in members:
        member.compute_api_address()
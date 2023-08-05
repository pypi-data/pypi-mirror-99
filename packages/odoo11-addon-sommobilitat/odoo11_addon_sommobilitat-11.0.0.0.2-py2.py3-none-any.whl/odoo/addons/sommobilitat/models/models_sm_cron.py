from odoo import models, api
from odoo.addons.sommobilitat.models.models_sommobilitat_utils import sommobilitat_utils


class sm_cron(models.Model):
  _name = 'sommobilitat.sm_cron'

  @api.model
  def fetch_members_from_wp(self):
    _sm_utils = sommobilitat_utils.get_instance()
    _sm_utils.fetch_wp_users(self)

  @api.model
  def activate_cooperative_member(self):
    members = self.env['res.partner'].search([
      ('member_nr', '>', 0),
      ('cooperative_member', '=', False)
    ])
    if members.exists():
      for member in members:
        member.activate_member()
from odoo import models, api
from odoo.addons.sommobilitat.models.models_sommobilitat_utils import sommobilitat_utils


class sm_member_fetch_wizard(models.TransientModel):
  _name = "sommobilitat.sm_member_fetch_wizard"

  @api.multi
  def create_request(self):
    _sm_utils = sommobilitat_utils.get_instance()
    _sm_utils.fetch_wp_users(self)
    return True

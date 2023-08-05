from odoo import models, fields, api
from odoo.tools.translate import _


class sm_maintenance_user(models.Model):
  _inherit = 'res.partner'
  _name = 'res.partner'

  maintenance_related_member = fields.Many2one('res.partner', string=_("Maintenance Related member"))

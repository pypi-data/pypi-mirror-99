from odoo import models, fields, api
from odoo.tools.translate import _


class sm_reporting_member(models.Model):
  _inherit = 'res.partner'
  _name = 'res.partner'

  reporting_related_member_id = fields.Many2one('res.partner', string=_("Reporting related member"))
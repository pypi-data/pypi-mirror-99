from odoo import models, fields, api
from odoo.tools.translate import _

from odoo.addons.sm_maintenance.models.models_sm_utils import sm_utils
from odoo.addons.sm_maintenance.models.models_sm_resources import sm_resources

class sm_member(models.Model):
  _inherit = 'res.partner'
  _name = 'res.partner'

  image_dni = fields.Char(string=_("DNI image"))
  driving_license_expiration_date = fields.Char(string=_("Driving license expiration date"))
  image_driving_license = fields.Char(string=_("Driving license image"))
  representative = fields.Char(string=_("Represented person "))
  representative_dni = fields.Char(string=_("Represented person DNI/NIF"))
  related_representative_member_id = fields.Many2one('res.partner',string=_("Related represented member"))
  birthday = fields.Date(string=_("Birthday"))
  # newsletter_subscription = fields.Boolean(string=_("Newsletter subscription"))

  # for email templates
  member_email_date = fields.Char(string=_("Current date"), compute='get_current_date', store=False)

  def get_current_date(self):
    for record in self:
      record.member_email_date = time.strftime("%d/%m/%Y")
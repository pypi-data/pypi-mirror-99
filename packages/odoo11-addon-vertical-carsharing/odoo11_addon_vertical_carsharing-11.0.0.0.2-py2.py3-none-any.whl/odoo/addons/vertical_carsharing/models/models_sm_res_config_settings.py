# -*- coding: utf-8 -*-
from odoo import fields, models, _

class ResConfigSettings(models.TransientModel):
  _inherit = 'res.config.settings'

  notfound_car_analytic_account_id = fields.Many2one(
    related='company_id.notfound_car_analytic_account_id',
    string=_("Not found car analytic account"))
  notfound_teletac_analytic_account_id = fields.Many2one(
    related='company_id.notfound_teletac_analytic_account_id',
    string=_("Not found teletac analytic account"))
  cs_invoice_payment_mode_id = fields.Many2one(
    related='company_id.cs_invoice_payment_mode_id',
    string=_("Payment Mode default for carsharing invoices"))

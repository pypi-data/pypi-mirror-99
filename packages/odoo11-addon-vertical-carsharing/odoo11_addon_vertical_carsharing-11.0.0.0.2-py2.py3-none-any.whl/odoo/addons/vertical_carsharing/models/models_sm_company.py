# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _


class sm_company(models.Model):
  _inherit = 'res.company'

  notfound_car_analytic_account_id = fields.Many2one('account.analytic.account',
    string=_("Not found car analytic account"))
  notfound_teletac_analytic_account_id = fields.Many2one('account.analytic.account',
    string=_("Not found teletac analytic account"))
  cs_invoice_payment_mode_id = fields.Many2one('account.payment.mode',
    string=_("Payment Mode default for carsharing invoices"))
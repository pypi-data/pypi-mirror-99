# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _


class sm_company(models.Model):
  _inherit = 'res.company'

  cs_carsharing_product_id = fields.Many2one('product.product',
    string=_("Carsharing product (predefined)"))
  cs_teletac_product_id = fields.Many2one('product.product',
    string=_("Teletac product (predefined)"))
  cs_discount_product_id = fields.Many2one('product.product',
    string=_("Discount product (predefined)"))

  invoice_mail_template_id = fields.Many2one('mail.template',
    string=_("Invoice notification template"))
  invoice_report_mail_template_id = fields.Many2one('mail.template',
    string=_("Invoice report notification template"))
  invoice_report_teletac_mail_template_id = fields.Many2one('mail.template',
    string=_("Invoice report teletac notification template"))
# -*- coding: utf-8 -*-
from odoo import fields, models, _

class ResConfigSettings(models.TransientModel):
  _inherit = 'res.config.settings'

  # INVOICING
  cs_carsharing_product_id = fields.Many2one(
    related='company_id.cs_carsharing_product_id',
    string=_("Carsharing product (predefined)"))
  cs_teletac_product_id = fields.Many2one(
    related='company_id.cs_teletac_product_id',
    string=_("Teletac product (predefined)"))
  cs_discount_product_id = fields.Many2one(
    related='company_id.cs_discount_product_id',
    string=_("Discount product (predefined)"))

  # MAIL TEMPLATES
  invoice_mail_template_id = fields.Many2one(
    related='company_id.invoice_mail_template_id',
    string=_("Invoice notification template"))
  invoice_report_mail_template_id = fields.Many2one(
    related='company_id.invoice_report_mail_template_id',
    string=_("Invoice report notification template"))
  invoice_report_teletac_mail_template_id = fields.Many2one(
    related='company_id.invoice_report_teletac_mail_template_id',
    string=_("Invoice report teletacs notification template"))

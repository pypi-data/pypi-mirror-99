# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _


class sm_member(models.Model):
  _inherit = 'res.partner'
  _name = 'res.partner'

  paymaster = fields.Many2one('res.partner', string=_("Paymaster for company reservations"))
  cs_monthly_fee = fields.Float(string=_("Carsharing monthly fee"))
  cs_monthly_fee_type = fields.Selection(
    [('add_to_pb', 'Add to pocketbook'),
     ('add_to_pb_and_pay', 'Add to pocketbook and pay it'),
     ('tariff_fee', 'Tariff fee')],
    _('Fee type'))
  invoicing_email = fields.Char(string=_("Invoicing email"))

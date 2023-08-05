# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _


class smp_reservation_compute(models.Model):
  _inherit = 'smp.sm_reservation_compute'
  _name = 'smp.sm_reservation_compute'

  # invoice_report_id = fields.Many2one('sm.invoice_report', string=_("Related invoice report"))
  report_reservation_compute_id = fields.Many2one('smp.sm_report_reservation_compute', string=_("Report"))

smp_reservation_compute()

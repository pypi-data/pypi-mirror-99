# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _


class sm_teletac(models.Model):
  _inherit = 'smp.sm_teletac'
  _name = 'smp.sm_teletac'

  invoice_report_id = fields.Many2one('sm.invoice_report', string=_("Related invoice report"))
  report_reservation_compute_id = fields.Many2one('smp.sm_report_reservation_compute', string=_("Report"))

  # @api.depends('invoice_report_id')
  # def report_reservation_compute_id(self):
  #   for record in self:
  #     if record.reservation_compute_id.id:
  #       record.reservation_compute_invoiced = record.reservation_compute_id.compute_invoiced
  #     else:
  #       record.reservation_compute_invoiced = False

  # @api.depends('invoice_report_id')
  # def _check_compute_forgiven(self):
  #   for record in self:
  #     if record.reservation_compute_id.id:
  #       record.reservation_compute_forgiven = record.reservation_compute_id.compute_forgiven
  #     else:
  #       record.reservation_compute_forgiven = False


sm_teletac()

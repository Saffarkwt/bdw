# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import models, api, fields


class srStockPicking(models.Model):
	_inherit = "stock.picking"

	def auto_fill_done_qty_from_reserved_qty(self):
		for move in self.move_ids_without_package:
			if not move.forecast_availability:
				continue
			move.quantity_done = move.forecast_availability
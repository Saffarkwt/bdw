from odoo import models

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def print_display_receipt(self):
        return {
            'type': 'ir.actions.report',
            'report_name': 'stock_display_receipt.report_display_receipt',
            'report_type': 'qweb-pdf',
            'model': 'stock.picking',
            'res_ids': self.ids,
        }

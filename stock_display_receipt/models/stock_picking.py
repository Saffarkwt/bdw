from odoo import models

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def print_display_receipt(self):
        return self.env.ref('stock_display_receipt.action_display_receipt_report').report_action(self)

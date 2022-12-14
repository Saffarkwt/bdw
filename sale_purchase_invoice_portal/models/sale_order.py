from odoo import models, api, fields


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    po_id = fields.Many2one('purchase.order',string="Purchase no")

    @api.onchange('product_id')
    def _onchange_po_id(self):
        line = self.po_id.order_line.search([('product_id','=',self.product_id.id)], limit=1, order='id desc')
        self.po_id = line.order_id if line else False

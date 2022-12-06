from odoo import models, api, fields


class AccountMove(models.Model):
    _inherit = "account.move"

    def is_consignment(self):
        po = self.purchase_id.search([('name','=',self.invoice_origin)])
        return True if po.is_consignment else False

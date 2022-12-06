from odoo.tests import Form
from odoo.fields import Date
from odoo import models, api, fields


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    is_consignment = fields.Boolean("Consignment")

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        action = self.picking_ids.button_validate()
        wizard = Form(self.env[action['res_model']].with_context(action['context'])).save()
        wizard.process()
        if not self.is_consignment:
            action = self.action_create_invoice()
            invoice = self.env['account.move'].browse(action['res_id'])
            invoice.invoice_date = Date.today()
            invoice.purchase_id = self.id
            invoice.action_post()
        return res

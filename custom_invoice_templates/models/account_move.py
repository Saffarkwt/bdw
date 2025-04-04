from odoo import api, fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_name_invoice_report(self):
        """
        This method is used to get the correct report name based on invoice type
        """
        self.ensure_one()
        if self.move_type == 'out_invoice':
            return 'custom_invoice_templates.report_sales_invoice'
        elif self.move_type == 'in_invoice':
            return 'custom_invoice_templates.report_purchase_invoice'
        return super()._get_name_invoice_report()

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    def action_print_invoice(self):
        """Print the invoice using the custom template based on invoice type and language"""
        self.ensure_one()
        
        # Clear report caches to ensure the latest template is used
        self.env['ir.actions.report']._clear_caches()
        
        # Determine the appropriate report based on invoice type and language
        if self.move_type == 'out_invoice':  # Sales Invoice
            if self.partner_id.lang == 'ar_001':
                report_name = 'custom_invoice_templates.action_report_sales_invoice_arabic'
            else:
                report_name = 'custom_invoice_templates.action_report_sales_invoice_english'
        elif self.move_type == 'in_invoice':  # Purchase Invoice
            if self.partner_id.lang == 'ar_001':
                report_name = 'custom_invoice_templates.action_report_purchase_invoice_arabic'
            else:
                # Force using a specific template for English purchase invoices
                return self.env.ref('custom_invoice_templates.action_report_purchase_invoice_english').report_action(self)
        else:
            raise UserError(_("This action is only available for invoices."))
        
        return self.env.ref(report_name).report_action(self)
    
    # Direct override of the print method for purchase invoices
    def _get_report_base_filename(self):
        """Override to provide custom filenames for invoice reports"""
        self.ensure_one()
        if self.move_type == 'out_invoice':
            return 'Sales Invoice - %s' % (self.name)
        elif self.move_type == 'in_invoice':
            return 'Purchase Invoice - %s' % (self.name)
        return super(AccountMove, self)._get_report_base_filename()
    
    # Override the default print behavior for purchase invoices
    def _get_name_invoice_report(self):
        """Override to force specific templates for purchase invoices"""
        self.ensure_one()
        if self.move_type == 'in_invoice':
            if self.partner_id.lang == 'ar_001':
                return 'custom_invoice_templates.report_purchase_invoice_arabic'
            else:
                return 'custom_invoice_templates.report_purchase_invoice_english'
        return super(AccountMove, self)._get_name_invoice_report()

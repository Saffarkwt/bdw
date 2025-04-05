from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    def _get_report_base_filename(self):
        self.ensure_one()
        if self.move_type == 'out_invoice':
            return 'Sales Invoice - %s' % (self.name)
        elif self.move_type == 'in_invoice':
            return 'Purchase Invoice - %s' % (self.name)
        else:
            return super(AccountMove, self)._get_report_base_filename()
    
    def get_invoice_report_by_lang(self):
        """
        Returns the appropriate report action based on invoice type and user language
        """
        self.ensure_one()
        lang = self.env.context.get('lang') or self.env.user.lang or 'en_US'
        is_arabic = lang.startswith('ar')
        
        if self.move_type == 'out_invoice':
            if is_arabic:
                return self.env.ref('custom_invoice_templates.action_report_sales_invoice_arabic')
            else:
                return self.env.ref('custom_invoice_templates.action_report_sales_invoice_english')
        elif self.move_type == 'in_invoice':
            if is_arabic:
                return self.env.ref('custom_invoice_templates.action_report_purchase_invoice_arabic')
            else:
                return self.env.ref('custom_invoice_templates.action_report_purchase_invoice_english')
        
        # Fallback to default report
        return None
        
    def action_print_invoice(self):
        """
        Direct method to print the appropriate invoice template based on invoice type
        This method bypasses the standard report selection mechanism
        """
        self.ensure_one()
        report_action = None
        
        # Clear report caches to ensure fresh templates are used
        self.env['ir.actions.report'].clear_caches()
        
        # Determine invoice type and language
        lang = self.env.context.get('lang') or self.env.user.lang or 'en_US'
        is_arabic = lang.startswith('ar')
        
        # Select appropriate report based on invoice type and language
        if self.move_type == 'out_invoice':  # Customer Invoice
            if is_arabic:
                report_action = self.env.ref('custom_invoice_templates.action_report_sales_invoice_arabic').report_action(self)
            else:
                report_action = self.env.ref('custom_invoice_templates.action_report_sales_invoice_english').report_action(self)
        elif self.move_type == 'in_invoice':  # Vendor Bill
            if is_arabic:
                report_action = self.env.ref('custom_invoice_templates.action_report_purchase_invoice_arabic').report_action(self)
            else:
                report_action = self.env.ref('custom_invoice_templates.action_report_purchase_invoice_english').report_action(self)
        
        # If no specific report found, use default
        if not report_action:
            report_action = self.env.ref('account.account_invoices').report_action(self)
            
        return report_action

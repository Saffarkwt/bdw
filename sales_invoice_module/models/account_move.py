from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    def _get_report_base_filename(self):
        self.ensure_one()
        if self.move_type == 'out_invoice':
            return 'Sales Invoice - %s' % (self.name)
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
                return self.env.ref('sales_invoice_module.action_report_sales_invoice_arabic')
            else:
                return self.env.ref('sales_invoice_module.action_report_sales_invoice_english')
        
        # Fallback to default report
        return None
        
    def action_print_sales_invoice(self):
        """
        Direct method to print the sales invoice template
        This method bypasses the standard report selection mechanism
        """
        self.ensure_one()
        report_action = None
        
        # Clear report caches to ensure fresh templates are used
        self.env['ir.actions.report'].clear_caches()
        
        # Determine language
        lang = self.env.context.get('lang') or self.env.user.lang or 'en_US'
        is_arabic = lang.startswith('ar')
        
        # Select appropriate report based on language
        if self.move_type == 'out_invoice':  # Customer Invoice only
            if is_arabic:
                report_action = self.env.ref('sales_invoice_module.action_report_sales_invoice_arabic').report_action(self)
            else:
                report_action = self.env.ref('sales_invoice_module.action_report_sales_invoice_english').report_action(self)
        
        # If no specific report found, use default
        if not report_action:
            report_action = self.env.ref('account.account_invoices').report_action(self)
            
        return report_action

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

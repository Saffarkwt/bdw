from odoo import models, fields, api, _

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    def action_print_purchase_invoice(self):
        """Print the purchase invoice using the standalone template"""
        self.ensure_one()
        
        # Clear report caches to ensure the latest template is used
        self.env['ir.actions.report']._clear_caches()
        
        # Only allow for purchase invoices
        if self.move_type != 'in_invoice':
            return
            
        # Return the purchase invoice report action
        return self.env.ref('purchase_invoice_standalone.action_report_purchase_invoice').report_action(self)

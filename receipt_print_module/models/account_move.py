from odoo import models, fields, api
from num2words import num2words

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    amount_total_words = fields.Char(string='Amount in Words', compute='_compute_amount_total_words')
    
    @api.depends('amount_total', 'currency_id')
    def _compute_amount_total_words(self):
        """Compute the total amount in words based on the currency"""
        for record in self:
            if record.amount_total:
                # Get amount as integer and decimal parts
                amount_str = '{:.2f}'.format(record.amount_total)
                amount_parts = amount_str.split('.')
                integer_part = int(amount_parts[0])
                
                # Convert to words based on currency
                if record.currency_id.name == 'KWD':
                    amount_in_words = num2words(integer_part, lang='en').title() + ' Dinar'
                    if integer_part != 1:
                        amount_in_words += 's'
                    
                    # Add decimal part if not zero
                    if int(amount_parts[1]) > 0:
                        decimal_part = int(amount_parts[1])
                        amount_in_words += ' and ' + num2words(decimal_part, lang='en').title() + ' Fils'
                else:
                    # Default for other currencies
                    amount_in_words = num2words(record.amount_total, lang='en').title()
                    amount_in_words += ' ' + record.currency_id.name
                
                record.amount_total_words = amount_in_words
            else:
                record.amount_total_words = ''
    
    def action_print_receipt(self):
        """
        Direct method to print the receipt template
        """
        self.ensure_one()
        
        # Only proceed if this is a posted invoice
        if self.state != 'posted':
            return False
        
        # Clear report caches to ensure fresh templates are used
        self.env['ir.actions.report'].clear_caches()
        
        # Get the receipt report action
        report_action = self.env.ref('receipt_print_module.action_report_receipt').report_action(self)
            
        return report_action

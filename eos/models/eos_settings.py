from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class EOSSettings(models.Model):
    _name = 'eos.settings'
    _description = 'End of Service Settings'
    
    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                default=lambda self: self.env.company)
    
    # Default values for EOS calculations
    default_days_per_year = fields.Integer(string='Default Days Per Year', default=30)
    default_days_per_month = fields.Integer(string='Default Days Per Month', default=30)
    
    # Accounting settings
    eos_expense_account_id = fields.Many2one('account.account', string='EOS Expense Account')
    eos_payable_account_id = fields.Many2one('account.account', string='EOS Payable Account')
    eos_journal_id = fields.Many2one('account.journal', string='EOS Journal')
    
    # Payment methods
    payment_method_ids = fields.Many2many('eos.payment.method', string='Payment Methods')
    
    _sql_constraints = [
        ('name_uniq', 'unique(name, company_id)', 'Settings name must be unique per company!')
    ]


class EOSPaymentMethod(models.Model):
    _name = 'eos.payment.method'
    _description = 'End of Service Payment Method'
    
    name = fields.Char(string='Name', required=True, translate=True)
    code = fields.Char(string='Code', required=True)
    active = fields.Boolean(default=True)
    
    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Payment method code must be unique!')
    ]

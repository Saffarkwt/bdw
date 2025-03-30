from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class HRContract(models.Model):
    _inherit = 'hr.contract'
    
    # EOS related fields
    eos_days = fields.Integer(string='EOS Days Balance', compute='_compute_eos_balance', store=True)
    eos_amount = fields.Float(string='EOS Amount Balance', compute='_compute_eos_balance', store=True, digits=(16, 2))
    leave_days = fields.Float(string='Leave Days Balance', compute='_compute_leave_balance', store=True, digits=(16, 2))
    leave_amount = fields.Float(string='Leave Amount Balance', compute='_compute_leave_balance', store=True, digits=(16, 2))
    
    @api.depends('employee_id', 'date_start', 'wage')
    def _compute_eos_balance(self):
        """Compute the current EOS balance for the employee based on service period"""
        for contract in self:
            if contract.employee_id and contract.date_start and contract.wage:
                # Calculate service period
                today = fields.Date.today()
                delta = relativedelta(today, contract.date_start)
                years_of_service = delta.years + (delta.months / 12) + (delta.days / 365)
                
                # Default calculation based on Kuwaiti labor law
                # First 5 years: 15 days per year
                # After 5 years: 26 days per year
                eos_days = 0
                if years_of_service <= 5:
                    eos_days = years_of_service * 15
                else:
                    eos_days = 5 * 15  # First 5 years
                    eos_days += (years_of_service - 5) * 26  # Remaining years
                
                contract.eos_days = int(eos_days)
                contract.eos_amount = contract.eos_days * (contract.wage / 30)
            else:
                contract.eos_days = 0
                contract.eos_amount = 0
    
    @api.depends('employee_id')
    def _compute_leave_balance(self):
        """Compute the current leave balance for the employee"""
        for contract in self:
            # This would need to be implemented based on the leave management system
            # For now, we'll set it to 0
            contract.leave_days = 0
            contract.leave_amount = 0

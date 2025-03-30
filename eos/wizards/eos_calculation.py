from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class EOSCalculation(models.TransientModel):
    _name = 'eos.calculation.wizard'
    _description = 'End of Service Calculation Wizard'
    
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    calculation_date = fields.Date(string='Calculation Date', required=True, default=fields.Date.context_today)
    reason_id = fields.Many2one('eos.reason', string='Termination Reason', required=True)
    
    # Results
    service_years = fields.Float(string='Service Years', compute='_compute_results', digits=(16, 2))
    service_days = fields.Integer(string='Service Days', compute='_compute_results')
    unpaid_leave_days = fields.Integer(string='Unpaid Leave Days', compute='_compute_results')
    net_service_days = fields.Integer(string='Net Service Days', compute='_compute_results')
    
    eos_days = fields.Integer(string='EOS Days', compute='_compute_results')
    eos_amount = fields.Float(string='EOS Amount', compute='_compute_results', digits=(16, 2))
    leave_days = fields.Float(string='Leave Days', compute='_compute_results', digits=(16, 2))
    leave_amount = fields.Float(string='Leave Amount', compute='_compute_results', digits=(16, 2))
    
    @api.depends('employee_id', 'calculation_date', 'reason_id')
    def _compute_results(self):
        for wizard in self:
            if wizard.employee_id and wizard.calculation_date and wizard.reason_id:
                # Get employee contract
                contract = wizard.employee_id.contract_id
                if not contract:
                    wizard.service_years = 0
                    wizard.service_days = 0
                    wizard.unpaid_leave_days = 0
                    wizard.net_service_days = 0
                    wizard.eos_days = 0
                    wizard.eos_amount = 0
                    wizard.leave_days = 0
                    wizard.leave_amount = 0
                    continue
                
                # Calculate service period
                from dateutil.relativedelta import relativedelta
                delta = relativedelta(wizard.calculation_date, contract.date_start)
                wizard.service_years = delta.years + (delta.months / 12) + (delta.days / 365)
                wizard.service_days = (wizard.calculation_date - contract.date_start).days + 1
                
                # Calculate unpaid leave days (simplified)
                wizard.unpaid_leave_days = 0
                
                # Calculate net service days
                wizard.net_service_days = wizard.service_days - wizard.unpaid_leave_days
                
                # Calculate EOS based on reason
                daily_wage = contract.wage / 30
                
                if wizard.reason_id.calculation_method == 'none':
                    wizard.eos_days = 0
                    wizard.eos_amount = 0
                elif wizard.reason_id.calculation_method == 'fixed':
                    wizard.eos_days = 0
                    wizard.eos_amount = wizard.reason_id.fixed_amount
                else:  # formula based
                    eos_days = 0
                    
                    # Apply formulas based on service years
                    for formula in wizard.reason_id.formula_ids:
                        if (formula.min_service_years <= wizard.service_years and 
                            (formula.max_service_years == 0 or wizard.service_years < formula.max_service_years)):
                            
                            # Calculate applicable years for this formula
                            if formula.min_service_years == 0 and formula.max_service_years > 0:
                                applicable_years = min(wizard.service_years, formula.max_service_years)
                            elif formula.min_service_years > 0 and formula.max_service_years > 0:
                                applicable_years = min(wizard.service_years, formula.max_service_years) - formula.min_service_years
                            elif formula.min_service_years > 0 and formula.max_service_years == 0:
                                applicable_years = wizard.service_years - formula.min_service_years
                            else:
                                applicable_years = wizard.service_years
                            
                            formula_days = applicable_years * formula.days_per_year
                            formula_days = formula_days * (formula.percentage / 100)
                            eos_days += formula_days
                    
                    wizard.eos_days = int(eos_days)
                    wizard.eos_amount = wizard.eos_days * daily_wage
                
                # Calculate leave balance (simplified)
                wizard.leave_days = 0
                wizard.leave_amount = 0
            else:
                wizard.service_years = 0
                wizard.service_days = 0
                wizard.unpaid_leave_days = 0
                wizard.net_service_days = 0
                wizard.eos_days = 0
                wizard.eos_amount = 0
                wizard.leave_days = 0
                wizard.leave_amount = 0
    
    def action_create_request(self):
        """Create an EOS request based on the calculation"""
        self.ensure_one()
        
        if not self.employee_id or not self.calculation_date or not self.reason_id:
            raise UserError(_('Please fill in all required fields.'))
        
        # Create EOS request
        request_vals = {
            'employee_id': self.employee_id.id,
            'request_date': fields.Date.today(),
            'termination_date': self.calculation_date,
            'reason_id': self.reason_id.id,
        }
        
        eos_request = self.env['eos.request'].create(request_vals)
        
        # Return action to view the created request
        return {
            'name': _('End of Service Request'),
            'view_mode': 'form',
            'res_model': 'eos.request',
            'res_id': eos_request.id,
            'type': 'ir.actions.act_window',
        }

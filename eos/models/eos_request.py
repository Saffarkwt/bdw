from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class EOSRequest(models.Model):
    _name = 'eos.request'
    _description = 'End of Service Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'request_date desc, id desc'
    
    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, 
                       default=lambda self: _('New'))
    
    # Company
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                default=lambda self: self.env.company)
    
    # Employee Information
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, 
                                  tracking=True, readonly=True, states={'draft': [('readonly', False)]})
    department_id = fields.Many2one('hr.department', string='Department', 
                                   related='employee_id.department_id', store=True)
    job_id = fields.Many2one('hr.job', string='Job Position', 
                            related='employee_id.job_id', store=True)
    employee_number = fields.Char(string='Employee Number', 
                                 related='employee_id.employee_number', store=True)
    
    # Dates
    request_date = fields.Date(string='Request Date', required=True, default=fields.Date.context_today, 
                              tracking=True, readonly=True, states={'draft': [('readonly', False)]})
    hire_date = fields.Date(string='Hire Date', related='employee_id.contract_id.date_start', 
                           store=True, readonly=True)
    termination_date = fields.Date(string='Termination Date', required=True, 
                                  tracking=True, readonly=True, states={'draft': [('readonly', False)]})
    notice_start_date = fields.Date(string='Notice Start Date', 
                                   tracking=True, readonly=True, states={'draft': [('readonly', False)]})
    
    # Reason
    reason_id = fields.Many2one('eos.reason', string='Termination Reason', required=True, 
                               tracking=True, readonly=True, states={'draft': [('readonly', False)]})
    
    # Service Calculation
    total_service_days = fields.Integer(string='Total Service Days', compute='_compute_service_period', store=True)
    total_service_years = fields.Float(string='Total Service Years', compute='_compute_service_period', store=True, digits=(16, 2))
    unpaid_leave_days = fields.Integer(string='Unpaid Leave Days', compute='_compute_unpaid_leaves', store=True)
    net_service_days = fields.Integer(string='Net Service Days', compute='_compute_service_period', store=True)
    
    # EOS Calculation
    eos_days = fields.Integer(string='EOS Days', compute='_compute_eos_amount', store=True)
    eos_amount = fields.Float(string='EOS Amount', compute='_compute_eos_amount', store=True, digits=(16, 2))
    
    # Leave Calculation
    leave_days = fields.Float(string='Leave Days', compute='_compute_leave_amount', store=True, digits=(16, 2))
    leave_amount = fields.Float(string='Leave Amount', compute='_compute_leave_amount', store=True, digits=(16, 2))
    
    # Salary Calculation
    salary_days = fields.Float(string='Salary Days', compute='_compute_salary_amount', store=True, digits=(16, 2))
    salary_amount = fields.Float(string='Salary Amount', compute='_compute_salary_amount', store=True, digits=(16, 2))
    
    # Additional Benefits
    ticket_amount = fields.Float(string='Ticket Amount', digits=(16, 2), readonly=True, states={'draft': [('readonly', False)]})
    bonus_amount = fields.Float(string='Bonus Amount', digits=(16, 2), readonly=True, states={'draft': [('readonly', False)]})
    
    # Total Settlement
    total_amount = fields.Float(string='Total Settlement', compute='_compute_total_amount', store=True, digits=(16, 2))
    
    # Payment Method
    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('check', 'Check'),
        ('transfer', 'Bank Transfer')
    ], string='Payment Method', default='transfer', required=True, 
       readonly=True, states={'draft': [('readonly', False)]})
    
    # State
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved by Manager'),
        ('hr_approved', 'Approved by HR'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True, copy=False)
    
    # Accounting
    move_id = fields.Many2one('account.move', string='Journal Entry', readonly=True, copy=False)
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('eos.request') or _('New')
        return super(EOSRequest, self).create(vals_list)
    
    @api.depends('employee_id', 'hire_date', 'termination_date', 'unpaid_leave_days')
    def _compute_service_period(self):
        for record in self:
            if record.hire_date and record.termination_date:
                delta = relativedelta(record.termination_date, record.hire_date)
                record.total_service_days = (record.termination_date - record.hire_date).days + 1
                record.total_service_years = delta.years + (delta.months / 12) + (delta.days / 365)
                record.net_service_days = record.total_service_days - record.unpaid_leave_days
            else:
                record.total_service_days = 0
                record.total_service_years = 0
                record.net_service_days = 0
    
    @api.depends('employee_id')
    def _compute_unpaid_leaves(self):
        for record in self:
            # This would need to be implemented based on the leave management system
            # For now, we'll set it to 0
            record.unpaid_leave_days = 0
    
    @api.depends('reason_id', 'net_service_days', 'employee_id.contract_id.wage')
    def _compute_eos_amount(self):
        for record in self:
            # This is a simplified calculation - the actual implementation would be more complex
            # based on the Kuwaiti labor law and the reason for termination
            if record.reason_id and record.net_service_days > 0 and record.employee_id.contract_id:
                daily_wage = record.employee_id.contract_id.wage / 30
                
                # Example calculation based on Kuwaiti labor law
                years_of_service = record.total_service_years
                
                if record.reason_id.calculation_method == 'none':
                    record.eos_days = 0
                    record.eos_amount = 0
                elif record.reason_id.calculation_method == 'fixed':
                    record.eos_days = 0
                    record.eos_amount = record.reason_id.fixed_amount
                else:  # formula based
                    eos_days = 0
                    
                    # Apply formulas based on service years
                    for formula in record.reason_id.formula_ids:
                        if (formula.min_service_years <= years_of_service and 
                            (formula.max_service_years == 0 or years_of_service < formula.max_service_years)):
                            
                            # Calculate applicable years for this formula
                            if formula.min_service_years == 0 and formula.max_service_years > 0:
                                applicable_years = min(years_of_service, formula.max_service_years)
                            elif formula.min_service_years > 0 and formula.max_service_years > 0:
                                applicable_years = min(years_of_service, formula.max_service_years) - formula.min_service_years
                            elif formula.min_service_years > 0 and formula.max_service_years == 0:
                                applicable_years = years_of_service - formula.min_service_years
                            else:
                                applicable_years = years_of_service
                            
                            formula_days = applicable_years * formula.days_per_year
                            formula_days = formula_days * (formula.percentage / 100)
                            eos_days += formula_days
                    
                    record.eos_days = int(eos_days)
                    record.eos_amount = record.eos_days * daily_wage
            else:
                record.eos_days = 0
                record.eos_amount = 0
    
    @api.depends('employee_id')
    def _compute_leave_amount(self):
        for record in self:
            # This would need to be implemented based on the leave management system
            # For now, we'll set it to 0
            record.leave_days = 0
            record.leave_amount = 0
    
    @api.depends('termination_date', 'employee_id.contract_id.wage')
    def _compute_salary_amount(self):
        for record in self:
            # Calculate remaining salary days in the month
            if record.termination_date and record.employee_id.contract_id:
                # Get the last day of the month
                last_day = record.termination_date.replace(day=28) + timedelta(days=4)
                last_day = last_day - timedelta(days=last_day.day)
                
                # Calculate remaining days
                remaining_days = (last_day - record.termination_date).days + 1
                
                if remaining_days > 0:
                    daily_wage = record.employee_id.contract_id.wage / 30
                    record.salary_days = remaining_days
                    record.salary_amount = remaining_days * daily_wage
                else:
                    record.salary_days = 0
                    record.salary_amount = 0
            else:
                record.salary_days = 0
                record.salary_amount = 0
    
    @api.depends('eos_amount', 'leave_amount', 'salary_amount', 'ticket_amount', 'bonus_amount')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = (record.eos_amount + record.leave_amount + 
                                  record.salary_amount + record.ticket_amount + 
                                  record.bonus_amount)
    
    def action_submit(self):
        self.write({'state': 'submitted'})
    
    def action_approve_manager(self):
        self.write({'state': 'approved'})
    
    def action_approve_hr(self):
        self.write({'state': 'hr_approved'})
    
    def action_pay(self):
        # This would create the accounting entries
        self.write({'state': 'paid'})
    
    def action_cancel(self):
        self.write({'state': 'cancelled'})
    
    def action_draft(self):
        self.write({'state': 'draft'})

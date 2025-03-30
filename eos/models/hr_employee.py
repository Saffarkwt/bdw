from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class HREmployee(models.Model):
    _inherit = 'hr.employee'
    
    # Add employee number field
    employee_number = fields.Char(string='Employee Number', copy=False)
    
    # EOS related fields
    eos_request_ids = fields.One2many('eos.request', 'employee_id', string='EOS Requests')
    eos_request_count = fields.Integer(string='EOS Request Count', compute='_compute_eos_request_count')
    
    @api.depends('eos_request_ids')
    def _compute_eos_request_count(self):
        for employee in self:
            employee.eos_request_count = len(employee.eos_request_ids)
    
    def action_view_eos_requests(self):
        self.ensure_one()
        return {
            'name': _('End of Service Requests'),
            'view_mode': 'tree,form',
            'res_model': 'eos.request',
            'domain': [('employee_id', '=', self.id)],
            'type': 'ir.actions.act_window',
            'context': {'default_employee_id': self.id}
        }
    
    # Method to get current EOS balance
    def get_eos_balance(self):
        self.ensure_one()
        contract = self.contract_id
        if contract:
            return {
                'days': contract.eos_days,
                'amount': contract.eos_amount
            }
        return {
            'days': 0,
            'amount': 0
        }
    
    # Method to get current leave balance
    def get_leave_balance(self):
        self.ensure_one()
        contract = self.contract_id
        if contract:
            return {
                'days': contract.leave_days,
                'amount': contract.leave_amount
            }
        return {
            'days': 0,
            'amount': 0
        }

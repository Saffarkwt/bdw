from odoo import http
from odoo.http import request

class EOSController(http.Controller):
    @http.route('/eos/dashboard', type='http', auth='user', website=True)
    def eos_dashboard(self, **kw):
        """Display EOS dashboard with summary information"""
        employee = request.env.user.employee_id
        
        if not employee:
            return request.render('eos.eos_dashboard_error', {
                'error_message': 'You are not linked to an employee record.'
            })
        
        # Get EOS requests
        eos_requests = request.env['eos.request'].search([
            ('employee_id', '=', employee.id)
        ])
        
        # Get EOS balance
        eos_balance = employee.get_eos_balance()
        leave_balance = employee.get_leave_balance()
        
        values = {
            'employee': employee,
            'eos_requests': eos_requests,
            'eos_balance': eos_balance,
            'leave_balance': leave_balance,
        }
        
        return request.render('eos.eos_dashboard_template', values)

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class EOSReason(models.Model):
    _name = 'eos.reason'
    _description = 'End of Service Reason'
    
    name = fields.Char(string='Reason', required=True, translate=True)
    code = fields.Char(string='Code', required=True)
    active = fields.Boolean(default=True)
    description = fields.Text(string='Description')
    
    # Company
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                default=lambda self: self.env.company)
    
    # Calculation method
    calculation_method = fields.Selection([
        ('fixed', 'Fixed Amount'),
        ('formula', 'Formula Based'),
        ('none', 'No Compensation')
    ], string='Calculation Method', default='formula', required=True)
    
    # Formula based calculation fields
    formula_ids = fields.One2many('eos.reason.formula', 'reason_id', string='Calculation Formulas')
    
    # Fixed amount calculation
    fixed_amount = fields.Float(string='Fixed Amount', digits=(16, 2))
    
    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Reason code must be unique!')
    ]


class EOSReasonFormula(models.Model):
    _name = 'eos.reason.formula'
    _description = 'End of Service Reason Formula'
    _order = 'sequence, id'
    
    reason_id = fields.Many2one('eos.reason', string='Reason', required=True, ondelete='cascade')
    sequence = fields.Integer(string='Sequence', default=10)
    name = fields.Char(string='Description', required=True)
    
    # Service period conditions
    min_service_years = fields.Float(string='Min Service Years', digits=(16, 2), default=0.0)
    max_service_years = fields.Float(string='Max Service Years', digits=(16, 2), default=0.0)
    
    # Calculation formula
    days_per_year = fields.Integer(string='Days Per Year', required=True, default=15)
    percentage = fields.Float(string='Percentage of Full Benefit', digits=(5, 2), default=100.0)
    
    @api.constrains('min_service_years', 'max_service_years')
    def _check_service_years(self):
        for record in self:
            if record.max_service_years > 0 and record.min_service_years > record.max_service_years:
                raise ValidationError(_('Minimum service years cannot be greater than maximum service years.'))

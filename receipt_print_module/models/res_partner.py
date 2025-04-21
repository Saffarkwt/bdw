from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    # Define civil_id field with more explicit parameters for cross-environment compatibility
    civil_id = fields.Char(
        string='Civil ID', 
        help='Civil ID number of the partner',
        copy=False,
        index=True,
        store=True,
        tracking=True
    )

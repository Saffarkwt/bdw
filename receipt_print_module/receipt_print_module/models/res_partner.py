from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    civil_id = fields.Char(string='Civil ID', help='Civil ID number of the partner')

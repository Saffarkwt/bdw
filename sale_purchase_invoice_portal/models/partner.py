from odoo import models, api, fields

class AccountMove(models.Model):
    _inherit = "res.partner"

    civil_id = fields.Char("Civil ID")
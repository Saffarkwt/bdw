from odoo import models, api, fields
class AccountMove(models.Model):
    _inherit = "account.move"

    civil_id = fields.Char(related="partner_id.email")
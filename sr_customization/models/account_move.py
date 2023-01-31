from odoo import models, api, fields,_
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = "account.move"

    civil_id = fields.Char(related="partner_id.email")
    invoice_num = fields.Char("Invoice Number",copy=False)

    @api.depends('posted_before', 'state', 'journal_id', 'date')
    def _compute_name(self):
        for move in self:
            if move.state == 'draft':
                move.name = '/'
            else:
                if not self.invoice_num:
                    if move.move_type == 'out_invoice':
                        sequence = self.env['ir.sequence'].search([('code','=','customer.invoice')])
                        if sequence:
                            move.name = sequence.next_by_id()
                            move.invoice_num = move.name
                        else:
                            raise UserError(_('Sequnce Not Found, May be you have deleted Sequence. \n Please update module to generate sequence'))
                    elif move.move_type == 'in_invoice' and not move.is_consignment:
                        sequence = self.env['ir.sequence'].search([('code','=','vendor.bill')])
                        if sequence:
                            move.name = sequence.next_by_id()
                            move.invoice_num = move.name
                        else:
                            raise UserError(_('Sequnce Not Found, May be you have deleted Sequence. \n Please update module to generate sequence'))
                    elif move.move_type == 'in_invoice' and move.is_consignment:
                        sequence = self.env['ir.sequence'].search([('code','=','display.invoice')])
                        if sequence:
                            move.name = sequence.next_by_id()
                            move.invoice_num = move.name
                        else:
                            raise UserError(_('Sequnce Not Found, May be you have deleted Sequence. \n Please update module to generate sequence'))
                    elif move.move_type == 'out_refund':
                        sequence = self.env['ir.sequence'].search([('code','=','return.invoice')])
                        if sequence:
                            move.name = sequence.next_by_id()
                            move.invoice_num = move.name
                        else:
                            raise UserError(_('Sequnce Not Found, May be you have deleted Sequence. \n Please update module to generate sequence'))
                    else:
                        return super(AccountMove, self)._compute_name()
                else:
                    move.name = move.invoice_num
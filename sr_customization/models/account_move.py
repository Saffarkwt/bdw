from odoo import models, api, fields,_
from odoo.exceptions import UserError
from lxml import etree


class AccountMove(models.Model):
    _inherit = "account.move"

    civil_id = fields.Char(related="partner_id.email")
    invoice_num = fields.Char("Invoice Number",copy=False)

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(AccountMove, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                       submenu=submenu)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            sale_reference = doc.xpath("//field[@name='state']")
            if self.env.context.get('default_move_type') == 'in_invoice':
                sale_reference[0].set("statusbar_visible", "draft,approved_state,posted")
            res['arch'] = etree.tostring(doc, encoding='unicode')
        return res

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
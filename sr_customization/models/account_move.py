from odoo import models, api, fields, _
from odoo.exceptions import UserError
from lxml import etree


class AccountMove(models.Model):
    _inherit = "account.move"

    civil_id = fields.Char(related="partner_id.email")
    invoice_num = fields.Char("Invoice Number", copy=False)

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        ##Sample Code of Hide print ,action menu and particular report
        res = super().fields_view_get(view_id, view_type, toolbar, submenu)
        print_report_id = False
        if self.env.context.get('default_move_type') == 'in_invoice':
            print_report_id = self.env.ref('sale_purchase_invoice_portal.account_purchase_invoice').id
        # if self.env.context.get('default_move_type')== 'out_refund':
        #     print_report_id = self.env.ref('sale_purchase_invoice_portal.account_purchase_invoice_refund').id
        if self.env.context.get('default_move_type') == 'out_invoice':
            print_report_id = self.env.ref('account.account_invoices').id
        if view_type == 'form' and print_report_id and toolbar and res['toolbar'] and res['toolbar'].get('print'):
            remove_report_record = [rec for rec in res['toolbar'].get('print') if rec.get('id') != print_report_id]
            if remove_report_record:
                for r in remove_report_record:
                    res['toolbar'].get('print').remove(r)
        return res

    @api.depends('posted_before', 'state', 'journal_id', 'date')
    def _compute_name(self):
        for move in self:
            if move.state == 'draft':
                move.name = '/'
            else:
                if not self.invoice_num:
                    if move.move_type == 'out_invoice':
                        sequence = self.env['ir.sequence'].search([('code', '=', 'customer.invoice')])
                        if sequence:
                            move.name = sequence.next_by_id()
                            move.invoice_num = move.name
                        else:
                            raise UserError(
                                _('Sequnce Not Found, May be you have deleted Sequence. \n Please update module to generate sequence'))
                    elif move.move_type == 'in_invoice' and not move.is_consignment:
                        sequence = self.env['ir.sequence'].search([('code', '=', 'vendor.bill')])
                        if sequence:
                            move.name = sequence.next_by_id()
                            move.invoice_num = move.name
                        else:
                            raise UserError(
                                _('Sequnce Not Found, May be you have deleted Sequence. \n Please update module to generate sequence'))
                    elif move.move_type == 'in_invoice' and move.is_consignment:
                        sequence = self.env['ir.sequence'].search([('code', '=', 'display.invoice')])
                        if sequence:
                            move.name = sequence.next_by_id()
                            move.invoice_num = move.name
                        else:
                            raise UserError(
                                _('Sequnce Not Found, May be you have deleted Sequence. \n Please update module to generate sequence'))
                    elif move.move_type == 'out_refund':
                        sequence = self.env['ir.sequence'].search([('code', '=', 'return.invoice')])
                        if sequence:
                            move.name = sequence.next_by_id()
                            move.invoice_num = move.name
                        else:
                            raise UserError(
                                _('Sequnce Not Found, May be you have deleted Sequence. \n Please update module to generate sequence'))
                    else:
                        return super(AccountMove, self)._compute_name()
                else:
                    move.name = move.invoice_num


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    extra_charges = fields.Float("Extra Charges", default=0.00)
    extra_charge_line_id = fields.Many2one("account.move.line")

    @api.onchange('extra_charges')
    def onchange_extra_charges(self):
        # self.price_subtotal += self.extra_charges
        # self.price_total += self.extra_charges
        # self.move_id.amount_untaxed += self.extra_charges
        # self.move_id.amount_total += self.extra_charges

        if self.extra_charges and not self.extra_charge_line_id:
            vals = {'name': str(self.name) + ' Repair',
                    'move_id': self.move_id._origin.id,
                    'account_id': self.account_id.id,
                    'debit': 0,
                    'credit': self.extra_charges,
                    'exclude_from_invoice_tab': True,
                    }
            line = self.env["account.move.line"].with_context(check_move_validity=False).create(vals)
            line._compute_analytic_account_id()
            existing_terms_lines = self.move_id.line_ids.filtered(
                lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))
            if existing_terms_lines:
                existing_terms_lines[0].debit = existing_terms_lines[0].debit + self.extra_charges
            self.extra_charge_line_id = line.id

        elif self.extra_charges and self.extra_charge_line_id:
            existing_terms_lines = self.move_id.line_ids.filtered(
                lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))
            if existing_terms_lines:
                existing_terms_lines[0].with_context(check_move_validity=False).debit = existing_terms_lines[
                                                                                            0].debit + self.extra_charges - self.extra_charge_line_id.credit
                self.extra_charge_line_id.with_context(check_move_validity=False, bypass=True).write(
                    {'credit': self.extra_charges})

        elif self.extra_charge_line_id:
            existing_terms_lines = self.move_id.line_ids.filtered(
                lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))
            if existing_terms_lines:
                existing_terms_lines[0].with_context(check_move_validity=False).debit = existing_terms_lines[
                                                                                            0].debit - self.extra_charge_line_id.credit
                line = self.extra_charge_line_id
                self.move_id.invoice_line_ids = [(2, line.id)]
                self.extra_charge_line_id = False
                # line.with_context(check_move_validity=False).unlink()
                # self.env.cr.execute("DELETE FROM ACCOUNT_MOVE_LINE WHERE ID=%s" % line.id)
                # self.env.cr.commit()

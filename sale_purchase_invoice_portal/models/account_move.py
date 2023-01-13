from odoo import models, api, fields, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    is_consignment = fields.Boolean(compute="compute_is_consignment",store=True)

    @api.depends('invoice_origin')
    def compute_is_consignment(self):
        for move in self:
            po = move.purchase_id.search([('name','=',move.invoice_origin)])
            move.is_consignment = True if po.is_consignment else False

    @api.depends('posted_before', 'state', 'journal_id', 'date')
    def _compute_name(self):
        for move in self:
            if move.is_consignment:
                if move.state == 'draft':
                    move.name = '/'
                else:
                    sequence = self.env['ir.sequence'].search([('code', '=', 'display.invoice')])
                    if sequence:
                        move.name = sequence.next_by_id()
                    else:
                        raise UserError(
                            _('Sequnce Not Found, May be you have deleted Sequence. \n Please update module to generate sequence'))
            else:
                return super(AccountMove,self)._compute_name()


    def _get_last_sequence_domain(self, relaxed=False):
        where_string, param = super(AccountMove,self)._get_last_sequence_domain()
        if self.is_consignment:
            where_string += " AND is_consignment = 't'"
        else:
            where_string += " AND is_consignment = 'f'"
        return where_string, param
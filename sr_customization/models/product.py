from odoo import models, api, fields


class Product(models.Model):
    _inherit = "product.product"
    _order = "create_date desc"

    @api.model_create_multi
    def create(self,vals):
        if self.env.context.get('default_type_product'):
            vals.update({'type':'consu', 'is_storable': True})
        res = super(Product,self).create(vals)
        return res

    @api.model
    def default_get(self, default_fields):
        values = super(Product, self).default_get(default_fields)
        values.update({'type': 'consu', 'is_storable': True})
        return values
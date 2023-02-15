from odoo import models, api, fields


class Product(models.Model):
    _inherit = "product.product"

    @api.model
    def create(self,vals):
        if self.env.context.get('default_type_product'):
            vals.update({'type':'product'})
        res = super(Product,self).create(vals)
        return res

    @api.model
    def default_get(self, default_fields):
        values = super(Product, self).default_get(default_fields)
        values.update({'type': 'product'})
        return values

class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def default_get(self, default_fields):
        values = super(ProductTemplate, self).default_get(default_fields)
        values.update({'detailed_type': 'product'})
        return values
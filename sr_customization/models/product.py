from odoo import models, api, fields


class Product(models.Model):
    _inherit = "product.product"

    @api.model
    def create(self,vals):
        if self.env.context.get('default_type_product'):
            vals.update({'type':'product'})
        res = super(Product,self).create(vals)
        return res
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


    def get_warranty(self):
        self.ensure_one()
        # This is a placeholder. You should customize this method to reflect how warranty information is stored and retrieved in your system.
        # For example, if warranty information is stored in a field named 'x_warranty_info':
        # if self.x_warranty_info:
        #     return self.x_warranty_info
        # else:
        #     return "لا يوجد ضمان متوفر لهذا المنتج"
        
        # Or, if warranty depends on product category or other logic:
        # if self.categ_id.name == 'Electronics':
        #     return "ضمان لمدة سنة واحدة للإلكترونيات"
        # else:
        #     return "الضمان القياسي للمنتج"
        
        # For now, returning a generic warranty string:
        return "معلومات الضمان للمنتج: " + self.name



    def get_cost_code(self):
        self.ensure_one()
        # This is a placeholder. You should customize this method to reflect how cost code information is stored and retrieved in your system.
        # For example, if cost code information is stored in a field named 'x_cost_code_info':
        # if self.x_cost_code_info:
        #     return self.x_cost_code_info
        # else:
        #     return "لا يوجد رمز تكلفة لهذا المنتج"
        
        # Or, if cost code depends on other product attributes or logic:
        # if self.standard_price > 1000:
        #     return "CC-HIGH"
        # else:
        #     return "CC-STD"
        
        # For now, returning a generic cost code string:
        return "رمز التكلفة للمنتج: " + self.name

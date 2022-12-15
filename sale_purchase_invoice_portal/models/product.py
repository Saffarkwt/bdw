from odoo import models, api, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def get_warranty(self):
        for line in self.attribute_line_ids:
            if line.attribute_id.name == 'Warranty date':
                return line.value_ids[0].name

    def get_cost_code(self):
        for line in self.attribute_line_ids:
            if line.attribute_id.name == 'Cost':
                return line.value_ids[0].name
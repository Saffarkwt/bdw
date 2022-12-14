from odoo import models, api, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def get_attributes(self):
        for line in self.attribute_line_ids:
            str = ''
            if line.attribute_id.name in ['Warranty date', 'Cost']:
                str += line.value_ids[0].name + ','
            return str

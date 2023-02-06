from odoo import api, models, fields


class ProductProduct(models.Model):
    _name = "product.product"
    _inherit = _name

    quotation_wizard_id = fields.Integer()

    def open_product_price(self):
        ctx = self._context.copy()
        ctx.update(
            {
                'default_price': self.lst_price,
                'default_quotation_wizard_id': self.quotation_wizard_id
            }
        )

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'product.price.wizard',
            'views': [
                [
                    self.env.ref("quotation.product_price_wizard_form").id,
                    'form']
            ],
            'context': ctx,
            'target': 'new'
        }

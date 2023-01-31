from odoo import fields, models, api


class ProductPriceWizard(models.TransientModel):
    _name = "product.price.wizard"

    price = fields.Float(
        string="Price"
    )

    quotation_wizard_id = fields.Integer()

    def quote(self):
        ctx = self._context.copy()
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'quotation.wizard',
            'views': [
                [
                    self.env.ref("quotation.quotation_wizard_form").id,
                    'form']
            ],
            'context': ctx,
            'target': 'new'
        }

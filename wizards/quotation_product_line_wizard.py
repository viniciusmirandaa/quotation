from odoo import fields, models, api


class QuotationProductLine(models.TransientModel):
    _name = "quotation.product.line.wizard"

    attribute_id = fields.Many2one(
        string="Attribute",
        comodel_name="product.attribute",
        readonly=True
    )

    alternative_product_tmpl_ids = fields.Many2many(
        related="attribute_id.alternative_product_ids"
    )

    alternative_product_product_ids = fields.Many2many(
        comodel_name="product.product",
        string="Alternative"
    )

    accessories_product_product_ids = fields.Many2many(
        string="Accessories",
        related="attribute_id.accessory_product_ids"
    )

    @api.onchange('attribute_id')
    def _onchange_attribute_id(self):
        if self.attribute_id:
            alternative_product_tmpl_ids = self.env['product.template'].browse(
                self.attribute_id.alternative_product_ids.ids)
            alternative_product_product_ids = self.env['product.product'].search(
                [('product_tmpl_id', 'in', alternative_product_tmpl_ids.ids)])

            return {'domain': {
                'alternative_product_product_ids': [('id', 'in', alternative_product_product_ids.mapped('id'))]
            }}

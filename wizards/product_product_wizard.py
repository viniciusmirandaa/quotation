from odoo import api, fields, models


class ProductProductWizard(models.TransientModel):
    _name = "product.product.wizard"

    product_product_id = fields.Many2one(
        comodel_name="product.product",
        ondelete="cascade",
        delegate=True
    )



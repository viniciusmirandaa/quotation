from odoo import models, fields, api


class QuotationWizard(models.TransientModel):
    _name = "quotation.wizard"

    customer_selection = fields.Selection(
        string="Customer Search",
        selection=[
            ('customer', 'Customer'),
            ('route', 'Route')
        ],
    )

    partner_id = fields.Many2one(
        string="Customer",
        comodel_name="res.partner",
        required=True
    )

    route_id = fields.Many2one(
        string="Route",
        comodel_name="routes",
        required=True
    )

    product_product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        required=True
    )

    quotation_product_line_ids = fields.One2many(
        comodel_name="quotation.product.line.wizard",
        inverse_name="quotation_id"
    )

    @api.onchange('route_id', 'partner_id')
    def onchange_customer_selection(self):
        if self.customer_selection == 'route' and self.route_id:
            customer_ids = self.env['res.partner'].search([('route_id', '=', self.route_id.id)])

            return {'domain': {
                'partner_id': [('id', 'in', customer_ids.ids)]
            }}

        if self.customer_selection == 'customer' and self.partner_id:
            self.route_id = self.partner_id.route_id.id

    @api.onchange('customer_selection')
    def _onchange_customer_selection(self):
        if self.customer_selection:
            self.route_id = False
            self.partner_id = False

            return {'domain': {
                'partner_id': [('id', 'in', self.env['res.partner'].search([]).ids)]
            }}

    def visualize_product(self):
        return

    def search_product(self):
        return

# {
#     'res_model': 'product.product.wizard',
#     'res_id': self.product_template_id.id,
#     'type': 'ir.actions.act_window',
#     'view_mode': 'form',
#     'view_id': self.env.ref('quotation.product_template_only_form_view').id,
#     "target": "current"
# }

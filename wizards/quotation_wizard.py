from odoo import models, fields, api


class QuotationWizard(models.TransientModel):
    _name = "quotation.wizard"

    # secondary variables

    get_product_domain = fields.Boolean()

    is_product_available = fields.Boolean()

    product_product_ids = fields.Many2many(
        comodel_name="product.product"
    )

    status = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('active', 'Active')
        ],
        default='draft'
    )

    # primary variables

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
    )

    quotation_product_line_ids = fields.Many2many(
        comodel_name="product.product",
        relation="quotation_products_product_product_rel"
    )

    quotation_product_accessories = fields.Many2many(
        comodel_name="product.product",
        relation="quotation_accessories_product_product_rel"
    )

    quotation_product_alternatives = fields.Many2many(
        comodel_name="product.product",
        relation="quotation_alternatives_product_product_rel"
    )

    search_products = fields.Char(
        string="Product",
        required=True
    )

    @api.onchange('get_product_domain')
    def _onchange_get_product_domain(self):
        if self.customer_selection and self.get_product_domain:
            if self.product_product_ids:
                self.is_product_available = True
                return {'domain': {
                    'product_product_id': [('id', 'in', self.product_product_ids.ids)]
                }}

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.customer_selection == 'customer' and self.partner_id and self.partner_id.route_id.id:
            self.route_id = self.partner_id.route_id.id

    @api.onchange('route_id')
    def onchange_route_id(self):
        if self.customer_selection == 'route' and self.route_id:
            customer_ids = self.env['res.partner'].search([('route_id', '=', self.route_id.id)])
            if self.partner_id.route_id != self.route_id:
                self.partner_id = False

            return {'domain': {
                'partner_id': [('id', 'in', customer_ids.ids)]
            }}

    @api.onchange('customer_selection')
    def _onchange_customer_selection(self):
        if self.customer_selection and not self.get_product_domain:
            self.route_id = False
            self.partner_id = False

            return {'domain': {
                'partner_id': [('id', 'in', self.env['res.partner'].search([]).ids)]
            }}

    def visualize_product(self):
        ctx = dict()
        ctx.update({
            'default_quotation_wizard_id': ctx.get('active_id'),
        })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.product_product_id.id,
            'res_model': 'product.product',
            'views': [
                [
                    self.env.ref("product.product_normal_form_view").id,
                    'form'
                ]
            ],
            'target': 'current',
            'context': ctx
        }

    def search_product(self):
        str_search = str(self.search_products)
        splited_search = str_search.split(" ")
        search_dict = {'domain': []}

        for word in splited_search:
            search_dict['domain'].append(('name', 'ilike', word))

        ctx = dict()
        ctx.update({
            'default_status': 'active',
            'default_customer_selection': self.customer_selection,
            'default_route_id': self.route_id.id,
            'default_partner_id': self.partner_id.id,
            'default_search_products': self.search_products,
            'default_get_product_domain': True,
            'default_product_product_ids': self.env['product.product'].search(search_dict['domain']).ids,
        })

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

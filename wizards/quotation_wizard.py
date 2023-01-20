from odoo import models, fields, api


class QuotationWizard(models.TransientModel):
    _name = "quotation.wizard"

    customer_selection = fields.Selection(
        string="Customer Search",
        selection=[
            ('customer', 'Customer'),
            ('route', 'Route')
        ],
        default=False
    )

    partner_id = fields.Many2one(
        string="Customer",
        comodel_name="res.partner",
        required=True
    )

    route_id = fields.Many2one(
        string="Route",
        comodel_name="routes",
    )

    @api.onchange('route_id')
    def _onchange_customer_selection(self):
        if self.customer_selection == 'route':
            customer_ids = self.env['res.partner'].search([('route_id', '=', self.route_id.id)])

            return {'domain': {
                'partner_id': [('id', 'in', customer_ids.ids)]
            }}

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.route_id = self.partner_id.route_id.id

    @api.onchange('customer_selection')
    def _onchange_customer_selection(self):
        if self.customer_selection:
            self.route_id, self.partner_id = False


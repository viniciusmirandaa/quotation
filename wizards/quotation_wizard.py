from odoo import models, fields, api


class QuotationWizard(models.TransientModel):
    _name = "quotation.wizard"

    customer_selection = fields.Selection(
        string="Customer Search",
        selection=[
            ('customer', 'Customer'),
            ('route', 'Route')
        ]
    )

    partner_id = fields.Many2one(
        string="Customer",
        comodel_name="res.partner",
        required=True
    )

    customer_route = fields.Many2one(
        string="Route",
        comodel_name="routes",
        default=lambda lm: lm._default_customer_route()
    )

    def _default_customer_route(self):
        if self.partner_id:
            return self.partner_id.route_id.id

    
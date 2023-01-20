from odoo import api, fields, models


class SearchProductProductWizard(models.TransientModel):
    _name = "search.product.product.wizard"

    context_name = fields.Char()

    

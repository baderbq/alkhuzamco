# -*- coding: utf-8 -*-
# Part of Alkhuzam & Co. - Morison Advisory . See LICENSE file for full copyright and licensing details.
from odoo import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def update_prices_(self):
        self.ensure_one()
        for line in self._get_update_prices_lines():
            line.product_uom_change()
            line.discount = 0  # Force 0 as discount for the cases when _onchange_discount directly returns
            line._onchange_discount()
        self.show_update_pricelist = False
        
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        super(SaleOrder, self).onchange_partner_id()
        self = self.with_company(self.company_id)
        values = {
            'pricelist_id': (self.sale_order_template_id and self.sale_order_template_id.pricelist_id.id) or (self.partner_id.property_product_pricelist and self.partner_id.property_product_pricelist.id) or False,
        }
        self.update(values)
        self.update_prices_()

    @api.onchange('sale_order_template_id')
    def onchange_sale_order_template_id(self):
        super(SaleOrder, self).onchange_sale_order_template_id()
        self = self.with_company(self.company_id)
        values = {
            'pricelist_id': (self.sale_order_template_id and self.sale_order_template_id.pricelist_id and self.sale_order_template_id.pricelist_id.id) or (self.partner_id.property_product_pricelist and self.partner_id.property_product_pricelist.id) or False,
        }
        self.update(values)
        self.update_prices_()
        
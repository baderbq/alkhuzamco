# -*- coding: utf-8 -*-
# Part of Alkhuzam & Co. - Morison Advisory . See LICENSE file for full copyright and licensing details.
from odoo import  fields, models

class SaleOrderTemplate(models.Model):
    _inherit = "sale.order.template"



    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', check_company=True,  # Unrequired company
                                   required=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", tracking=1,help="If you change the pricelist, only newly added lines will be affected.")



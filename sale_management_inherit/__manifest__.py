# -*- coding: utf-8 -*-
# Part of Alkhuzam & Co. - Morison Advisory . See LICENSE file for full copyright and licensing details.
{
    'name': 'Quotation template pricelists',
    'version': '15.0.0.1',
    'category': 'Sales/Sales',
    'sequence': 5,
    'summary': 'Quotation Template Pricelist',
    "author": "Alkhuzam & Co. - Morison Advisory",
    'description': """
    Manage pricelist foreach quotation Template
    ============================================

    This application allows you to manage pricing based of the quotation templates, 
    using the selected pricelist in the template

    ***Quotation Templates ** -> **Price List** 
    """,
    'website': 'https://www.alkhuzam.com',
    'depends': ['sale_management'],
    'data': ['views/sale_order_template_views.xml'],
    'demo': [
    ],
    'price': 5,
    'currency': 'USD',
    "installable": True,
    'application': False,
    'license': 'LGPL-3',
    "images": ["static/description/Banner.png"],
    #"live_test_url": 'https://youtu.be/fk9dY53I9ow',
}

# -*- coding: utf-8 -*-
#############################################################################
#
#
#############################################################################

{
    'name': 'Quotation Approval',
    'version': '15.0.1.1.0',
    'category': 'Sales Management',
    #'live_test_url': 'https://www.youtube.com/watch?v=CigmHe9iC4s&feature=youtu.be',
    'summary': "Quotation Approval by users",
    "author": "Alkhuzam & Co., Yahla Rida",
    'website': 'https://www.alkhuzam.com',
    'description': """

Quotation Approval
=======================
Module to manage Quotation Approval.
""",
    'depends': ['sale'],
    'data': [
        'views/sale_view.xml',
        'views/res_config_view.xml',

    ],
    #'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'application': True,
    'installable': True,
    'auto_install': False,
}

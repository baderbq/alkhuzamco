# coding: utf-8 
{
    'name': 'Kuwait - Payroll A',
    'author': 'Morison Global - Alkhuzam & Co - RIDA YAHLA',
    'category': 'Human Resources/Payroll',
    'description': """
Kuwait Payroll and End of Service rules Accounts.
========================================
    """,
    'depends': ['account','l10n_kw_hr_payroll'],
    'data': [
        'views/account_move_views.xml',
        'report/eos_leaves_reporting.xml',
        'security/ir.model.access.csv',
    ],
    'assets': {
        'web.assets_backend': [
            'l10n_kw_hr_payroll_account/static/src/js/**/*',
        ],
        'web.assets_qweb': [
            'l10n_kw_hr_payroll_account/static/src/xml/**/*',
        ],
    },
    'license': 'OEEL-1',
    'auto_install': False,
}

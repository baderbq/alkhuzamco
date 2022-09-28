# coding: utf-8 
{
    'name': 'Kuwait - Payroll',
    'author': 'Alkhuzam & Co',
    'category': 'Human Resources/Payroll',
    'description': """
Kuwait Payroll and End of Service rules.
========================================
This module is created for odoo payroll in kuwait.
    """,
    'depends': ['hr_payroll'],
    'data': [
        'data/hr_payroll_structure_type_data.xml',
        'data/hr_payroll_structure_data.xml',
        'data/hr_salary_rule_data.xml',
        'views/hr_contract_views.xml',
        'views/hr_employee_public_views.xml',
        'report/hr_contract_history_report_views.xml'
    ],
    'license': 'OEEL-1',
    'auto_install': False,
}

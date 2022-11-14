# coding: utf-8 
{
    'name': 'Kuwait - Payroll',
    'version': '15.0.0.1',
    "author": "Alkhuzam & Co. - Morison Advisory",
    'summary': 'Kuwait Payroll and End of Service rules.',
    'category': 'Human Resources/Payroll',
    'description': """
Kuwait Payroll and End of Service rules.
========================================
Configuration of hr_payroll for kuwait localization
Calculating the basic salary for the employees following the kuwait law.
Calculating the end of service and provision
Daily computation of leaves and end of service for each contracted employee.
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
    'license': 'OPL-1',
    "installable": True,
    'auto_install': False,
    'application':True,
    'price': 100,
    'currency': 'USD',
    'images': ['static/description/banner.gif'],
    'company': 'Alkhuzam & Co.- Morison Advisory',
    'maintainer': 'Alkhuzam & Co.- Morison Advisory',
}

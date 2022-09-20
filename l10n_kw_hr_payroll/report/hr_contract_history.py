# -*- coding: utf-8 -*-

from odoo import  fields, models, _



class ContractHistory(models.Model):
    _inherit = 'hr.contract.history'


    # Even though it would have been obvious to use the reference contract's id as the id of the
    # hr.contract.history model, it turned out it was a bad idea as this id could change (for instance if a
    # new contract is created with a later start date). The hr.contract.history is instead closely linked
    # to the employee. That's why we will use this id (employee_id) as the id of the hr.contract.history.

    anual_leave_salary = fields.Monetary(string="Leaves",related="employee_id.anual_leave_salary")
    eos_indiminity = fields.Monetary(string="EOS indiminity",related="employee_id.eos_indiminity")



   
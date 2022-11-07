# -*- coding: utf-8 -*-

from odoo import  fields, models, _



class ContractHistory(models.Model):
    _inherit = 'hr.contract.history'



    anual_leave_salary = fields.Monetary(string="Leaves",related="employee_id.anual_leave_salary")
    eos_indiminity = fields.Monetary(string="EOS indiminity",related="employee_id.eos_indiminity")



   
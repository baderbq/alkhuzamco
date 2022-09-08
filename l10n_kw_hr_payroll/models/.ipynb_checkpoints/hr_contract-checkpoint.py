#coding: utf-8
from odoo import models, fields, api, _


class HRContract(models.Model):
    _inherit = "hr.contract"

    over_time_coef = fields.Float(string="OverTime Coef",help="This field used to get overworking time cost/hour, cost_OVT = OverTime Coef * hour_cost",default=1.0)
    #fils_rounding_payslip = fields.Float(string="Fils Rounding",help="This field used to specify the rounding base, EXP:0.05 will round the salary Net based on 50 Fils.")
    departure_reason_id = fields.Many2one("hr.departure.reason",related="employee_id.departure_reason_id")
    housing_allowance = fields.Monetary(string="Housing Allowance")
    transportation_allowance = fields.Monetary(string="Transportation Allowance")
    other_allowances = fields.Monetary(string="Other Allowances")
    basic_number_of_days = fields.Integer(string="Number of Days", help="Number of days of basic salary.",default=26)



    @api.onchange('company_id')
    def _onchange_company_id(self):
        if self.company_id:
            structure_types = self.env['hr.payroll.structure.type'].search([
                ('country_id', '=', self.company_id.country_id.id)])
            if structure_types:
                self.structure_type_id = structure_types[0]
            elif self.structure_type_id not in structure_types:
                self.structure_type_id = False
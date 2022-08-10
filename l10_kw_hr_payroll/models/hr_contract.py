#coding: utf-8
from odoo import models, fields


class HRContract(models.Model):
    _inherit = "hr.contract"

    over_time_coef = fields.Float(string="OverTime Coef",help="This field used to get overworking time cost/hour, cost_OVT = OverTime Coef * hour_cost")
    fils_rounding_payslip = fields.Float(string="Fils Rounding",help="This field used to specify the rounding base, EXP:0.05 will round based on 50 Fils.")
    departure_reason_id = fields.Many2one("hr.departure.reason",related="employee_id.departure_reason_id")



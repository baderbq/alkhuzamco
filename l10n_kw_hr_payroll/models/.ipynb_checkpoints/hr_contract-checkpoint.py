#coding: utf-8
from odoo import models, fields, api, _
from datetime import datetime, timedelta, time
from odoo.exceptions import UserError, ValidationError
class HRContract(models.Model):
    _inherit = "hr.contract"

    over_time_coef = fields.Float(string="OverTime Coef",help="This field used to get overworking time cost/hour, cost_OVT = OverTime Coef * hour_cost",default=1.0)
    #fils_rounding_payslip = fields.Float(string="Fils Rounding",help="This field used to specify the rounding base, EXP:0.05 will round the salary Net based on 50 Fils.")
    departure_reason_id = fields.Many2one("hr.departure.reason",related="employee_id.departure_reason_id")
    housing_allowance = fields.Monetary(string="Housing Allowance")
    transportation_allowance = fields.Monetary(string="Transportation Allowance")
    other_allowances = fields.Monetary(string="Other Allowances")
    basic_number_of_days = fields.Integer(string="Number of Days", help="Number of days of basic salary.",default=26)
    anual_leave_salary = fields.Monetary(string="Annual leave until today",compute="get_an_leave_salary",help="The amount of accrued leaves until today")
    eos_indiminity = fields.Monetary(string="EOS indiminity until today",compute="end_of_service",help="The amount of End of service indiminity until today.")
    anual_leave_days = fields.Float(string="Annual leave Days",compute="get_an_leave_salary",help="The number of days of accrued leaves until today")
    eos_indiminity_days = fields.Float(string="EOS Days",compute="end_of_service",help="The number of worked days today.")
    leave_taken = fields.Float(string="taken leaves",compute="get_an_leave_salary",help="The amount of accrued leaves until today")



    @api.onchange('company_id')
    def _onchange_company_id(self):
        if self.company_id:
            structure_types = self.env['hr.payroll.structure.type'].search([
                ('country_id', '=', self.company_id.country_id.id)])
            if structure_types:
                self.structure_type_id = structure_types[0]
            elif self.structure_type_id not in structure_types:
                self.structure_type_id = False
    
    @api.depends('date_start','date_end')
    def get_an_leave_salary(self):
        for rec in self:
            start_date = rec.date_start
            end_date = datetime.now().date() if datetime.now().date()< rec.date_end else rec.date_end
            start = datetime.combine(start_date, datetime.min.time())
            stop = datetime.combine(end_date, datetime.max.time())
            day_rate = float( rec.wage /rec.basic_number_of_days)
            difference = (((end_date-start_date).days)/365)*30
            out_days, out_hours = 0, 0
            if start < stop:
                out_hours = list(rec._get_work_hours(start, stop, domain=['|', ('work_entry_type_id.code', '=', 'LEAVE105'), ('work_entry_type_id.code', '=', 'LEAVE100')]).items())
                out_hours = sum(oh[1] for oh in out_hours if oh and len(oh)>0)
                out_days += round(out_hours/rec.resource_calendar_id.hours_per_day)
            rec.anual_leave_days = (end_date-start_date).days
            rec.leave_taken = out_days
            rec.anual_leave_salary = (day_rate  * difference) - (day_rate  * out_days)

    
    @api.depends('date_start','date_end')
    def end_of_service(self):
        for rec in self:
            start_date = rec.first_contract_date
            end_date = datetime.now().date() if datetime.now().date()< rec.date_end else rec.date_end
            compensation = rec.wage + rec.housing_allowance + rec.transportation_allowance + rec.other_allowances
            day_rate = float( compensation /rec.basic_number_of_days)
            worked_days = (end_date-start_date).days
            worked_years = float(worked_days /365)
            eos_limit = compensation * 18
            # After 5 years computing
            eos = 0
            if worked_years <=5 :
                eos = worked_years * 15 * day_rate

            if worked_years >5:
                ra = worked_years -5
                eos= (75 * day_rate )+ (compensation*ra)
                
            result= eos if eos < eos_limit else eos_limit
            result = rec.company_id.currency_id.round(result)
            rec.eos_indiminity_days = worked_days
            rec.eos_indiminity = result
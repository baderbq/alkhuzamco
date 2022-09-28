from odoo import _, api, fields, models
from odoo.exceptions import UserError
from datetime import datetime


class eos_leaves_report(models.TransientModel):
    _name = 'eos.leaves.line'
    _description = 'EOS and leaves line'
    
    employee_id  = fields.Many2one('hr.employee',string="Employee")
    emp_status  = fields.Boolean(string="Employee Status",related="employee_id.active")
    contract_id = fields.Many2one('hr.contract',related="employee_id.contract_id")
    job_id = fields.Many2one(related="employee_id.job_id")
    first_contract_date = fields.Date(string="From Join Date",related="employee_id.first_contract_date",store=True)
    eos_report_id = fields.Many2one("eos.leaves.report","Report ID")
    end_date = fields.Date("To this date",related="eos_report_id.end_date")
    contract_end_date = fields.Date("Contract EndDate",related="contract_id.date_end")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    currency_id = fields.Many2one(string="Currency", related='company_id.currency_id', readonly=True)
    wage = fields.Monetary('Salary', related="contract_id.wage",store=True)
    
    total_allowences = fields.Monetary("Total Allowances", compute="get_total_allowances",store=True)
    
    deserved_leave_amount = fields.Monetary("Deserved Leave Salary ", compute="get_leave_amount",store=True,compute_sudo=True)
    
    deserved_eos_amount = fields.Monetary("Deserved EOS", compute="end_of_service",store=True,compute_sudo=True)
    resigned_eos_amount = fields.Monetary("Resign EOS", compute="end_of_service",compute_sudo=True)
    
    
    worked_days = fields.Float("Worked days", compute="get_leave_amount",compute_sudo=True)
    leave_taken = fields.Float(string="taken leaves",compute="get_an_leave_salary",help="The amount of accrued leaves until Date to",compute_sudo=True)
    
    @api.depends('contract_id')
    def get_total_allowances(self):
        for rec in self:
            rec.total_allowences = rec.contract_id and (rec.contract_id.housing_allowance+rec.contract_id.transportation_allowance+rec.contract_id.other_allowances)
    
    @api.depends('end_date')
    def get_leave_amount(self):
        for rec in self:
            contract = rec.contract_id
            start_date = contract.first_contract_date if contract.first_contract_date else contract.date_start or datetime.now().date() 
            end_date = contract.date_end if contract.date_end and rec.end_date > contract.date_end else rec.end_date
            start = datetime.combine(start_date, datetime.min.time())
            stop = datetime.combine(end_date, datetime.max.time()) if end_date else datetime.now()
            day_rate = float( contract.wage /(contract.basic_number_of_days or 26))
            difference = (((end_date-start_date).days)/365)*30 
            out_days, out_hours = 0, 0
            if start < stop and contract:
                out_hours = list(contract._get_work_hours(start, stop, domain=['|', ('work_entry_type_id.code', '=', 'LEAVE105'), ('work_entry_type_id.code', '=', 'LEAVE100')]).items())
                out_hours = sum(oh[1] for oh in out_hours if oh and len(oh)>0)
                out_days += round(out_hours/(contract.resource_calendar_id.hours_per_day or 8))
            rec.worked_days = (end_date-start_date).days
            rec.worked_days = rec.worked_days if rec.worked_days>=0 else 0
            rec.leave_taken = out_days
            rec.deserved_leave_amount = (day_rate  * difference) - (day_rate  * out_days)
            
    def new_report(self):
        return {
            'name':  'New Report of End of service and leave',
            'view_mode': 'form',
            'view_id': False,
            'res_model': 'eos.leaves.report',
            'context': dict(self._context),
            'type': 'ir.actions.act_window',
            'target': 'new',
            #'res_id': self.check_id,
            }
            
    @api.depends('end_date')
    def end_of_service(self):
        for rec in self:
            start_date = rec.first_contract_date if rec.first_contract_date else datetime.now().date()
            end_date = rec.end_date if rec.end_date else datetime.now().date()
            compensation = rec.wage + rec.total_allowences
            day_rate = float( compensation /(rec.contract_id and rec.contract_id.basic_number_of_days or 26) )
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
                
            #EOS departure computing cases ( 3/12= 0.25  => 3 month test of contract )
            resign_eos= 0
            if 0.25 < worked_years < 3:
                resign_eos= 0
            elif 3 <= worked_years <= 5:
                resign_eos= eos* 1 / 2 
            elif  5 < worked_years < 10:
                resign_eos= eos* 2 / 3
            else:
                result= eos if eos < eos_limit else eos_limit
                resign_eos = result
            resign_eos = rec.company_id.currency_id.round(resign_eos)
            rec.deserved_eos_amount = rec.company_id.currency_id.round(eos)
            rec.resigned_eos_amount = resign_eos
            

class eos_leaves_report(models.TransientModel):
    _name = 'eos.leaves.report'
    _description = 'EOS and leaves report'
    
    
    end_date = fields.Date("Report Date",default=fields.Date.today(),required=True)
    eos_leaves_lines = fields.One2many('eos.leaves.line','eos_report_id')
    department_id = fields.Many2one('hr.department',string="Department")
    only_active = fields.Boolean('Include active employee only ?',help="Check if you want to include only the active employees, and exlude archived ones.")
    
    @api.depends('only_active','department_id')
    def get_domain(self):
        domain=[]
        if self.department_id:
            domain.append(('department_id','=',self.department_id.id))
        if self.only_active : 
            domain.append(('active','=',self.only_active))
        else:
            domain.append(('active','in',[True,False]))
        return domain
    
    def clear_lines(self):
        self._cr.execute("delete from eos_leaves_line;")
        
    def action_generate_eos_leave_report(self):
        eos_leave_obj = self.env['eos.leaves.line']
        self.clear_lines()
        for emp in self.env['hr.employee'].search(self.get_domain()):
            eos_leave_obj.create({"employee_id":emp.id,"eos_report_id":self.id})
        return True
        
        
        
    
    
    
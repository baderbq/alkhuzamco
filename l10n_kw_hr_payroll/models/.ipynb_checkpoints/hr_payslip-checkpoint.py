# coding: utf-8 
from odoo import models

class HRPayslip(models.Model):
    _inherit = 'hr.payslip'
    
    #Kuwait Basic salary calculation
    def _get_paid_amount(self):
        _super = super()._get_paid_amount()
        if self.contract_id.country_code == "KW":
            day_rate = float( self.contract_id.wage /self.contract_id.basic_number_of_days)
            hour_rate = float(day_rate / 8)
            try:
                unpaid_hours = sum([line.number_of_hours for line in self.worked_days_line_ids if line.work_entry_type_id and line.work_entry_type_id.id in self.struct_id.unpaid_work_entry_type_ids.ids])
                if unpaid_hours <= 40:
                    return self.contract_id.wage - (unpaid_hours * hour_rate )
                else:
                    return _super
            except:
                return _super
        else:
            return _super


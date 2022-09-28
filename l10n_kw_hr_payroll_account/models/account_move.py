# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    employee_id  = fields.Many2one('hr.employee',string="Employee")
    payslip_id = fields.Many2one('hr.payslip',string="PaySlip",compute="compute_payslip")
    contract_id  = fields.Many2one('hr.contract',related="payslip_id.contract_id")
    
    
    def compute_payslip(self):
        for rec in self:
            slip = self.env['hr.payslip'].search([('move_id','=',rec.id)],limit=1)
            rec.payslip_id = slip and slip.id
            rec.employee_id = rec.payslip_id and rec.payslip_id.employee_id.id
            
    # -------------------------------------------------------------------------
    # OVERRIDE METHODS
    # -------------------------------------------------------------------------

    def get_payslip(self):
        self.ensure_one()
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Linked Payslip',
            'res_model': 'hr.payslip',
            'view_mode': 'form',
            'res_id': self.payslip_id.id,
        }
        if not self.payslip_id:
            action = True
        return action
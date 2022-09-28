# -*- coding: utf-8 -*-

from odoo import fields, models
import logging

_logger = logging.getLogger(__name__)

class DataCleaner(models.Model):
    _name = 'data.cleaner'
    
    name= fields.Char('Reference')
    modules = fields.Many2many('ir.module.module',domain=[('application','=',True)])
    state = fields.Selection([('draft','Draft'),('confirm','Confirmed')])
    
    def delete_data(self):
        try:
            for module in self.modules:
                
        except:
            _logger.debug('Error when trying to execute delete_data methode', exc_info=True)
    
    def delete_crm(self):
        crm_data = "delete from public.crm_lead;delete from public.ir_attachment where res_model in ('crm.lead');delete from public.mail_message where model in ('crm.lead');delete from public.mail_activity where res_model in ('crm.lead');alter SEQUENCE crm_lead_id_seq restart with 1; delete from mail_followers where res_model in ('crm.lead')"
        
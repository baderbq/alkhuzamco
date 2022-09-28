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
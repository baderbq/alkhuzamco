# -*- coding: utf-8 -*-
#############################################################################
#
#
#############################################################################

from odoo import api, fields, models
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    approved = fields.Boolean("Approved",tracking=1)
    company_approval = fields.Boolean("Company approvals",related="company_id.so_order_approval")

    def action_confirm(self):
        if self.company_id.so_order_approval == False or (self.company_id.so_order_approval == True and self.approved == True):
            super(SaleOrder, self).action_confirm()
        else:
            if self.company_id.so_order_approval == True and self.approved == False:
                app_names = ""
                for approver in self.company_id.approver_ids:
                    app_names = "- "+str(approver.name)+".\n"
                raise UserError("You are not allowed to confirm non approved quotation, You can ask one of the following users for approval :\n"+app_names)

    def action_quotation_send(self):
        if self.company_id.so_order_approval == False or (self.company_id.so_order_approval == True and self.approved == True):
            return super(SaleOrder, self).action_quotation_send()
        else:
            if self.company_id.so_order_approval == True and self.approved == False:
                app_names = ""
                for approver in self.company_id.approver_ids:
                    app_names = "- "+str(approver.name)+".\n"
                raise UserError("You are not allowed to send non approved quotation, You can ask one of the following users for approval :\n"+app_names)


    def action_approve(self):
        if self.company_id.so_order_approval and self.company_id.approver_ids:
            if self._uid in  self.company_id.approver_ids.ids:
                self.approved = True
            else:
                raise UserError("You have no right to approve quotations\n")
        else:
            return False

        return True

    def request_approve(self):
        msg="""<h2 style="overflow-y: hidden;"><a title="Click to check this Quotation" style="background-color: #875A7B; padding: 4px 8px 4px 8px; text-decoration: none; color: #fff; border-radius: 5px; font-size:13px;" href="#" data-oe-model="sale.order" data-oe-id="%s">%s</a> </h2> """ % (str(self.id),str(self.name))

        message = "Hello,<br/>"+ self.env.user.name+" has request approval for Quotation N°"+str(msg)
        chanel_obj = self.env['mail.channel']
        
        if self.company_id.so_order_approval and self.company_id.approver_ids:
            for user in  self.company_id.approver_ids:
                odoobot_id = user.partner_id.id
                channel_info = chanel_obj.channel_get([odoobot_id])
                channel = chanel_obj.browse(channel_info['id'])
                channel.sudo().message_post(body=message, author_id=self.env.user.partner_id.id, message_type="notification", subtype_xmlid="mail.mt_comment")
                #raise UserError("You have no right to approve quotations\n")
        else:
            return False

        return True

class Company(models.Model):
    _inherit = 'res.company'

    so_order_approval = fields.Boolean("Quotation Approval")
    approver_ids = fields.Many2many('res.users',string="The approvers")


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    so_order_approval = fields.Boolean("Quotation Approval", related='company_id.so_order_approval',readonly=False)
    approver_ids =  fields.Many2many(related='company_id.approver_ids', relation='res.users', readonly=False)
 
    

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        

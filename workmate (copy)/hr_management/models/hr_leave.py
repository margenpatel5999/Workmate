from odoo import fields, api, models
from odoo.http import request
from odoo.exceptions import ValidationError


class HrLeaveDocument(models.Model):
    _name = 'leave.document'
    _description = "Hr Leave Document"

    name = fields.Char('Name')
    attachment = fields.Binary('Attachment')
    hr_leave_id = fields.Many2one('hr.leave', 'Hr leave id')


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    states = fields.Selection(
        [('draft', 'Draft'),
         ('waiting_for_approval', 'Waiting For Approval'),
         ('approved', 'Approved'),
         ('rejected', 'Rejected')], default='draft')

    url = fields.Char()

    leave_attachment_ids = fields.One2many('leave.document', 'hr_leave_id', 'Attachment')

    def send_to_manager(self):
        emp_rec = self.env['hr.employee'].sudo().search([('id', '=', self.employee_id.id)])
        email_ids = emp_rec.parent_id.work_email
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        base_url += '/web#id=%d&view_type=form&model=%s' % (self.id, self._name)
        self.url = base_url
        template = self.env.ref('hr_management.leave_email_template')
        print('\n\n\n\n\ntemplate', email_ids)
        email_values = {'email_to': email_ids, 'email_from': self.env.user.email or ''}
        template.send_mail(self.id, email_values=email_values, force_send=True,
                           email_layout_xmlid='mail.mail_notification_light')
        self.states = 'waiting_for_approval'

    def approved(self):
        if self.employee_id.parent_id.user_id.id == self.env.user.id:
            self.states = 'waiting_for_approval'
            emp_rec = self.env['hr.employee'].sudo().search([('id', '=', self.employee_id.id)])
            email_ids = emp_rec.work_email
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            base_url += '/web#id=%d&view_type=form&model=%s' % (self.id, self._name)
            self.url = base_url
            template = self.env.ref('hr_management.leave_approve_email_template')
            print('\n\n\n\n\ntemplate', email_ids)
            email_values = {'email_to': email_ids, 'email_from': self.env.user.email or ''}
            template.send_mail(self.id, email_values=email_values, force_send=True,
                               email_layout_xmlid='mail.mail_notification_light')
            self.states = 'approved'
        else:
            raise ValidationError('You are not manager of this employee.')

    def rejected(self):
        if self.employee_id.parent_id.user_id.id == self.env.user.id:
            self.states = 'waiting_for_approval'
            emp_rec = self.env['hr.employee'].sudo().search([('id', '=', self.employee_id.id)])
            email_ids = emp_rec.work_email
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            base_url += '/web#id=%d&view_type=form&model=%s' % (self.id, self._name)
            self.url = base_url
            template = self.env.ref('hr_management.leave_reject_email_template')
            print('\n\n\n\n\ntemplate', email_ids)
            email_values = {'email_to': email_ids, 'email_from': self.env.user.email or ''}
            template.send_mail(self.id, email_values=email_values, force_send=True,
                               email_layout_xmlid='mail.mail_notification_light')
            self.states = 'rejected'
        else:
            raise ValidationError('You are not manager of this employee.')

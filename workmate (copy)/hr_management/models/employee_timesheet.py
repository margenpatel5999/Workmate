from odoo import fields, api, models
from datetime import datetime, time, date, timedelta
from odoo.http import request
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    timesheet_id = fields.Many2one('employee.timesheet')


class EmployeeTimesheet(models.Model):
    _name = 'employee.timesheet'
    _rec_name = 'week_name'

    @api.model
    def default_get(self, fields):
        res = super(EmployeeTimesheet, self).default_get(fields)
        my_date = date.today()
        year, week_num, day_of_week = my_date.isocalendar()
        monday = my_date - timedelta(days=my_date.weekday())
        saturday = datetime.now().date() + timedelta(days=((datetime.now().isoweekday() + 1) % 7))
        employee_id = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)])
        res.update({'start_date': monday,
                    'end_date': saturday,
                    'week_name': str(year) + '-Week-' + str(week_num),
                    'employee_id': employee_id.id,

                    })
        return res

    start_date = fields.Date()
    end_date = fields.Date()
    week_name = fields.Char()
    employee_id = fields.Many2one('hr.employee')
    approved_by_rejected = fields.Many2one('hr.employee')
    timesheet_line_ids = fields.One2many('account.analytic.line', 'timesheet_id')
    state = fields.Selection(
        [('draft', 'Draft'),
         ('waiting_for_approval', 'Waiting For Approval'),
         ('approved', 'Approved'),
         ('rejected', 'Rejected')], default='draft')
    url = fields.Char()

    def send_to_manager(self):
        self.state = 'waiting_for_approval'
        emp_rec = self.env['hr.employee'].sudo().search([('id', '=', self.employee_id.id)])
        email_ids = emp_rec.parent_id.work_email
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        base_url += '/web#id=%d&view_type=form&model=%s' % (self.id, self._name)
        self.url = base_url
        template = self.env.ref('hr_management.manager_email_template')
        email_values = {'email_to': email_ids, 'email_from': self.env.user.email or ''}
        template.send_mail(self.id, email_values=email_values, force_send=True,
                           email_layout_xmlid='mail.mail_notification_light')

    def approved(self):
        if self.employee_id.parent_id.user_id.id == self.env.user.id:
            self.state = 'approved'
        else:
            raise ValidationError('You are not manager of this employee.')

    def rejected(self):
        self.state = 'rejected'

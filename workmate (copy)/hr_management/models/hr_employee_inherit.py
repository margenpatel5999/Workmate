from odoo import fields, api, models
import datetime

class ProjectProject(models.Model):
    _inherit = 'project.project'


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    address = fields.Char('Address')
    city_id = fields.Char('City')
    state_id = fields.Many2one('res.country.state')

    @api.onchange('country_id')
    def _onchange_country_id(self):
        res = {}
        res['domain'] = {'state_id': [('country_id', '=', self.country_id.id)]}
        return res

    def birthday_email(self):
        records = self.env['hr.employee'].search([])
        for record in records:
            if record.birthday:
                month = record.birthday.strftime("%m")
                day = record.birthday.strftime("%d")
                check_month = datetime.date.today().strftime("%m")
                check_day = datetime.date.today().strftime("%d")
                if day == check_day and month == check_month:
                    print('\n\n\n\n\ncall birthday')
                    # template_id = env['sms.template'].search([('name', '=', 'Birthdate Sms Template')])
                    # content = env['sms.template'].render_template(template_id.template_body, 'res.partner', record.id)
                    # account_id = env['sms.number'].search([('id', '=', 4)], limit=1)
                    # env['sms.api'].smsapi(account_id.account_id, record.mobile, content, record.id, 'res.partner',
                    #                       account_id, False, False)
                    email_ids = record.work_email
                    print(email_ids)

                    template = self.env.ref('hr_management.birthdate_email_template')
                    print(template)
                    email_values = {'email_to': email_ids, 'email_from': self.env.user.email or ''}
                    template.send_mail(record.id, email_values=email_values, force_send=True,
                                       email_layout_xmlid='mail.mail_notification_light')

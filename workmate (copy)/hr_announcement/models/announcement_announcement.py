from odoo import api, fields, models
from datetime import date
from odoo.exceptions import ValidationError


class AnnouncementAnnouncement(models.Model):
    _name = 'announcement.announcement'
    _description = "Hr Announcement"
    _rec_name = 'name'

    @api.model
    def default_get(self, fields):
        res = super(AnnouncementAnnouncement, self).default_get(fields)
        res.update({'company_id': self.env.user.company_id.id})
        return res

    name = fields.Char('Name', default='New')
    general_announcement = fields.Boolean('General Announcement')
    title = fields.Text('Title')
    description = fields.Html('Description')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    announcement_type = fields.Selection([
        ('employee', 'By Employee'), ('department', ' By Department'), ('job_position', ' By Job Position')
    ], 'Announcement Type')
    employee_ids = fields.Many2many("hr.employee", "rel_emp_announs", "emp_id", "anounce_id", string='Employee')
    department_ids = fields.Many2many("hr.department", "rel_dep_announs", "dep_id", "anounce_id", string='Department')
    job_ids = fields.Many2many("hr.job", "rel_job_announs", "job_id", "anounce_id", string='Job')
    requested_date = fields.Date('Requested Date', default=date.today())
    company_id = fields.Many2one('res.company', 'Company')
    attachment_ids = fields.One2many('announcement.document', 'announcement_id', 'Attachment')
    state = fields.Selection([
        ('draft', 'Draft'), ('waiting_for_approval', 'Waiting For Approval'), ('approved', 'Approved')
    ], default='draft')

    @api.model
    def create(self, vals):
        if vals:
            seq_obj = self.env['ir.sequence']
            name = seq_obj.next_by_code('announcement.announcement')
            vals.update({'name': name})
        res = super(AnnouncementAnnouncement, self).create(vals)
        return res

    @api.constrains('start_date', 'end_date')
    def start_end_date_constrains(self):
        if self.end_date < self.start_date:
            raise ValidationError('You Will Not Enter Start Date Smaller Then End Date')

    def sent_approval(self):
        self.state = 'waiting_for_approval'

    def approved(self):
        self.state = 'approved'

    def action_send_email(self):
        email_ids = ''
        if self.general_announcement == 'True':
            emp_ids = self.env['hr.employee'].search([])
            for emp_id in emp_ids:
                email_ids += emp_id.work_email + ','
        else:
            if self.employee_ids:
                for emp_line in self.employee_ids:
                    email_ids += emp_line.work_email + ','

            elif self.department_ids:
                emp_dep_ids = self.env['hr.employee'].search([('department_id', 'in', self.department_ids.ids)])
                for emp_dep_id in emp_dep_ids:
                    email_ids += emp_dep_id.work_email + ','

            elif self.job_ids:
                emp_job_ids = self.env['hr.employee'].search([('job_id', 'in', self.job_ids.ids)])
                for emp_job_id in emp_job_ids:
                    email_ids += emp_job_id.work_email + ','

        template = self.env.ref('hr_announcement.employee_email_template')
        email_values = {'email_to': email_ids, 'email_from': self.env.user.email or ''}
        template.send_mail(self.id, email_values=email_values, force_send=True,
                           email_layout_xmlid='mail.mail_notification_light')

    def action_send_email(self):
        email_id = ''
        if self.general_announcement == 'True':
            emp_ids = self.env['hr.employee'].search([])
            for emp_id in emp_ids:
                email_id += emp_id.work_email + ','
        else:
            if self.employee_ids:
                for emp_line in self.employee_ids:
                    email_id += emp_line.work_email + ','

            if self.department_ids:
                emp_dep_ids = self.env['hr.employee'].search([('department_id', 'in', self.department_ids.ids)])
                for emp_dep_id in emp_dep_ids:
                    email_id += emp_dep_id.work_email + ','

            if self.job_ids:
                emp_job_ids = self.env['hr.employee'].search([('job_id', 'in', self.job_ids.ids)])
                for emp_job_id in emp_job_ids:
                    email_id += emp_job_id.work_email + ','

        vals = {
            'subject': self.name,
            'body_html': self.title,
            'email_to': email_id,
            'auto_delete': False,
            'email_from': 'shubhpatel211099@gmail.com',
        }
        mail_id = self.env['mail.mail'].sudo().create(vals)
        mail_id.sudo().send()

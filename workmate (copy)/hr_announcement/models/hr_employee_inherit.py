from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def hr_announcement_smart_button(self):
        return {
            'name': 'Announcement',
            'type': 'ir.actions.act_window',
            'res_model': 'announcement.announcement',
            'view_mode': 'tree',
            'domain': ['|', '|', '|', ('employee_ids', '=', self.id),
                       ('job_ids', '=', self.job_id.id),
                       ('department_ids', '=', self.department_id.id),
                       ('general_announcement', '=', True),
                       ('state', '=', 'approved')],
        }

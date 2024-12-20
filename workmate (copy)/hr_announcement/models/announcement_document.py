from odoo import api, fields, models


class AnnouncementDocument(models.Model):
    _name = 'announcement.document'
    _description = "Announcement Document"
    _rec_name = 'name'

    name = fields.Char('Name')
    attachment = fields.Binary('Attachment')
    announcement_id = fields.Many2one('announcement.announcement', 'Announcement')

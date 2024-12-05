from odoo import fields, models
from datetime import datetime


class Feedback(models.Model):
    _name = "feedback"
    _description = "some model for feedback"

    name = fields.Char(required=False, string="Отправитель")
    review = fields.Text(required=True, string="Комментарий")
    send_time = fields.Datetime(string='Send Time', default=lambda self: fields.Datetime.now())


    file = fields.Binary(required=False, string="Файлы")

    def create_stats(self, form_type):
        # Используем self для доступа к текущему объекту
        self.env['stats'].create({
            'name': self.name,
            'send_time': self.send_time,
            'comment': self.comment,
            'file': self.file,
            'form_type': form_type,
        })

    def send(self):
        self.create_stats('feedback')
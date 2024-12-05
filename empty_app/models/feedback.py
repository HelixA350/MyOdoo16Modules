from odoo import fields, models

class Feedback(models.Model):
    _name = "feedback"
    _description = "some model for feedback"

    name = fields.Char(required=False, string="Отправитель")
    review = fields.Text(required=True, string="Комментарий")

    file = fields.Binary(required=False, string="Файлы")

    def send(self):
        pass
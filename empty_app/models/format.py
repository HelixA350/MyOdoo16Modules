from odoo import fields, models

class Format(models.Model):
    _name = "format"
    _description = "some model for testing"

    name = fields.Char(required=True, string="Имя")

    file_f = fields.Binary(required=False, string='Форматировать')

    def send(self):
        pass
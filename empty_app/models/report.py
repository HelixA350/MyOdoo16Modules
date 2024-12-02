from odoo import fields, models
from odoo import http
from odoo.http import request

class Report(models.Model):
    _name = "report"
    _description = "some model for testing"

    name = fields.Char(required=True, string="Имя")

    file_b = fields.Binary(required=False, string='Файл Битрикс')
    file_w = fields.Binary(required=False, string='Файл Веб-Системы')

    def send(self):
        pass



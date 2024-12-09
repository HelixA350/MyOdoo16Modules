from odoo import fields, models, api
from odoo import http
from odoo.http import request
from datetime import datetime


class Report(models.Model):
    _name = "report"
    _description = "some model for testing"

    name = fields.Char(required=False, string="Имя")
    send_time = fields.Datetime(string='Send Time', default=lambda self: fields.Datetime.now())


    file_b = fields.Binary(required=False, string='Файл Битрикс')
    file_w = fields.Binary(required=False, string='Файл Веб-Системы')

    
    def send(self):
        self.create_stats('report')
        

    def create_stats(self, form_type):
        self.env['stats'].create({
            'name': self.name,
            'send_time': self.send_time,
            'form_type': form_type,
        })

    def download(self):
        pass



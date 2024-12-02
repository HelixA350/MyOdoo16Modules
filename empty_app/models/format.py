from odoo import fields, models
from odoo import models, fields, api
import base64
import openpyxl
import io
import logging

_logger = logging.getLogger(__name__) 

class Format(models.Model):
    _name = "format"
    _description = "some model for testing"

    name = fields.Char(required=True, string="Имя")

    file_f = fields.Binary(required=True, string='Форматировать')

    def send(self):
        file_data = base64.b64decode(self.file_f)  # Декодируем переданный файл
        xlsx_data = io.BytesIO(file_data)  # Конвертируем в поток

        

        _logger.info('success')
        return None
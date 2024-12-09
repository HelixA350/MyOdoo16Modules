from odoo import fields, models
from odoo import models, fields, api
import base64
import openpyxl
import io
import logging
from .exlWrapper import ExcelWrapper
from .xl_work_class import Xl_work
import openpyxl as oxl
from datetime import datetime

_logger = logging.getLogger(__name__) 

class Format(models.Model):
    _name = "format"
    _description = "some model for testing"

    name = fields.Char(required=False, string="Имя")
    send_time = fields.Datetime(string='Send Time', default=lambda self: fields.Datetime.now())


    file_f = fields.Binary(required=True, string='Форматировать')

    def create_stats(self, form_type):
        # Используем self для доступа к текущему объекту
        self.env['stats'].create({
            'name': self.name,
            'send_time': self.send_time,
            'form_type': form_type,
        })


    def format_file(self, path_file:str, path_done:str) -> str:
        ew = ExcelWrapper(['Вложения', 'Последний раз обновлено', 'Статус', 'Наименование сервисного центра'], ['ПЭ: дата время', 'ПЭ: Комментарий', 'ПЭ: наработка м/ч'], path_file)
        ew.format()
        wb = oxl.load_workbook(filename=path_file)
        for sheet in wb.sheetnames[2:]:
            ew.formatTitles(wb[sheet], True)
            ew.formattingCells(wb[sheet])
        wb.save(path_done)
        wb.close()

    def send(self):
        file_data = base64.b64decode(self.file_f)  # Декодируем переданный файл
        xlsx_data = io.BytesIO(file_data)  # Конвертируем в поток
        
        self.format_file(xlsx_data, xlsx_data)
        self.send_time = datetime.now()

        self.create_stats('report')

        _logger.info('success')
        return None
    
    def download(self):
        pass
from odoo import fields, models
from odoo import models, fields, api
import base64
import openpyxl
import io
import logging
from .exlWrapper import ExcelWrapper
from .xl_work_class import Xl_work
import openpyxl as oxl

_logger = logging.getLogger(__name__) 

class Format(models.Model):
    _name = "format"
    _description = "some model for testing"

    name = fields.Char(required=True, string="Имя")

    file_f = fields.Binary(required=True, string='Форматировать')

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

        _logger.info('success')
        return None
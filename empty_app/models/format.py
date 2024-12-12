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
    add_avr_time = fields.Boolean(string='Считать среднюю наработку')
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
        # Установим время отправки
        self.send_time = datetime.now()

        # Создаем статистику
        self.create_stats('report')

        # Теперь перенаправляем пользователя на маршрут для скачивания обработанного файла
        return {
            'type': 'ir.actions.act_url',
            'url': f'/your_module/download_formating?model_id={self.id}',  # Указываем ID записи
            'target': 'self',
        }
    
    def download(self):
        # Путь к вашему файлу на сервере
        file_path = r'files/finished_report (7).xlsx'
        
        with open(file_path, 'rb') as file:
            file_content = file.read()

        return {
            'type': 'ir.actions.act_url',
            'url': 'data:text/plain;base64,' + base64.b64encode(file_content).decode(),
            'target': 'self',
            'download': True,
            'filename': 'downloaded_file.xlsx',
        }
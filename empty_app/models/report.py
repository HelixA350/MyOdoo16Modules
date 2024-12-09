from odoo import fields, models, api
from odoo import http
from odoo.http import request
from datetime import datetime
from .exlWrapper import ExcelWrapper
from .xl_work_class import Xl_work

class Report(models.Model):
    _name = "report"
    _description = "some model for testing"

    name = fields.Char(required=False, string="Имя")
    send_time = fields.Datetime(string='Send Time', default=lambda self: fields.Datetime.now())


    file_b = fields.Binary(required=False, string='Файл Битрикс')
    file_w = fields.Binary(required=False, string='Файл Веб-Системы')

    
    def send(self):
        # Установим время отправки
        self.send_time = datetime.now()

        # Создаем статистику
        self.create_stats('report')

        # Теперь перенаправляем пользователя на маршрут для скачивания обработанного файла
        return {
            'type': 'ir.actions.act_url',
            'url': f'/your_module/download_creating?model_id={self.id}',  # Указываем ID записи
            'target': 'self',
        }
        
    def merge_files(self, path_web:str, path_bitrix:str, path_done:str) -> (str, str):
        """Соединяет 2 загруженных файла в единый отчет, используя классы Xl_work и ExcelWrapper

        Args:
            path_bitrix (str): Путь к файлу с выгрузской из Битрикса
            path_web (str): Путь к файлу с выгрузкой из Веб-системы
            path_done (str): Путь к итоговому файл

        Returns:
            str: Возвращает значение ошибки, которое используется для вывода в всплывающем окне
            если ошибок нет, то значение - пустая строка
            str: Возвращает отладочное сообщение
        """
        xl = Xl_work(path_web, path_bitrix, path_done)
        if xl.error == '':
            ew = ExcelWrapper(['Вложения', 'Последний раз обновлено', 'Статус', 'Наименование сервисного центра'], ['ПЭ: дата время', 'ПЭ: Комментарий', 'ПЭ: наработка м/ч'], path_web)
            ew.format()
            xl.start()
            wb = xl.open_file(path_done)
            for sheet in wb.sheetnames[2:]:
                ew.formatTitles(wb[sheet], True)
                ew.formattingCells(wb[sheet])
            wb.save(path_done)
            wb.close()
            # xl.department_stat()
        # return xl.error, xl.message

    def create_stats(self, form_type):
        self.env['stats'].create({
            'name': self.name,
            'send_time': self.send_time,
            'form_type': form_type,
        })

    def download(self):
        pass



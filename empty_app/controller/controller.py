from odoo import http
from odoo.http import request
import base64
import io
import logging

_logger = logging.getLogger(__name__)

class DownloadController(http.Controller):
    @http.route('/your_module/download_formating', type='http', auth='user', methods=['GET'], csrf=True)
    def download_file(self, model_id, **kwargs):
        # Получаем объект записи из указанной модели
        record = request.env['format'].browse(int(model_id))
        
        # Декодируем файл и готовим потоки
        file_data = base64.b64decode(record.file_f)
        xlsx_data_input = io.BytesIO(file_data)
        xlsx_data_output = io.BytesIO()

        # Вызываем функцию format_file из модели
        record.format_file(xlsx_data_input, xlsx_data_output)

        # Получаем содержимое обработанного файла
        xlsx_content = xlsx_data_output.getvalue()

        # Логируем успешный результат
        _logger.info(f'Processed file downloaded for record ID {model_id}')

        # Возвращаем файл клиенту
        return request.make_response(
            xlsx_content,
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', 'attachment; filename="processed_file.xlsx"'),
            ]
        )
    
class DownloadController2(http.Controller):
    @http.route('/your_module/download_creating', type='http', auth='user', methods=['GET'], csrf=True)
    def download_file(self, model_id, **kwargs):
        # Получаем объект записи из указанной модели
        record = request.env['report'].browse(int(model_id))
        
        # Декодируем файл и готовим потоки
        file_data_b = base64.b64decode(record.file_b)
        xlsx_data_input_b = io.BytesIO(file_data_b)

        file_data_w = base64.b64decode(record.file_w)
        xlsx_data_input_w = io.BytesIO(file_data_w)
        xlsx_data_output = io.BytesIO()

        # Вызываем функцию format_file из модели
        record.merge_files(xlsx_data_input_w, xlsx_data_input_b, xlsx_data_output)

        # Получаем содержимое обработанного файла
        xlsx_content = xlsx_data_output.getvalue()

        # Логируем успешный результат
        _logger.info(f'Processed file downloaded for record ID {model_id}')

        # Возвращаем файл клиенту
        return request.make_response(
            xlsx_content,
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', 'attachment; filename="processed_file.xlsx"'),
            ]
        )

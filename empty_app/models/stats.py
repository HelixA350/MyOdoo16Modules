from odoo import fields, models
from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__) 

class Stats(models.Model):
    _name = "stats"
    _description = "model for showing statistics"

    # Импорт данных из report
    def get_my_model_data(self):
        report_records = self.env['report'].search([])
        for record in report_records:
            _logger.info(record.field1, record.field2)  # Вывод данных в консоль или дальнейшая обработка
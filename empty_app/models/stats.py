from odoo import fields, models
from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__) 

class Stats(models.Model):
    _name = "stats"
    _description = "model for showing statistics"

    name = fields.Char(string='Name')
    send_time = fields.Datetime(string='Sendtime')
    comment = fields.Text(string='Comment')
    form_type = fields.Selection([
        ('report', 'Report'),
        ('format', 'Format'),
        ('feedback', 'Feedback'),
        ], string='Form Type')
    file = fields.Binary(string='File')

    # Импорт данных из report
    def get_my_model_data(self):
        
        _logger.info()


        

        
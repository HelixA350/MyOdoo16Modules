from odoo import fields, models

class SomeModel(models.Model):
    _name = "some_model"
    _description = "some model for testing"

    name = fields.Char(required=True)
    password = fields.Char(required=True)
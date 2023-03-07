from odoo import api, fields, models


class SahamValue(models.Model):
    _name = 'ksp.saham.value'
    _description = 'Saham Value'
    _order = 'id desc'

    date_value = fields.Datetime(default=fields.Date.today)
    value = fields.Float()
    saham_id = fields.Many2one(comodel_name="kspsaham", string="", required=False, )

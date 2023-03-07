from odoo import api, fields, models


class TabunganLineType(models.Model):
    _name = 'ksp.tabungan.line.type'
    _rec_name = 'name'
    _description = 'Tabungan Line Type'
    _order = 'id desc'

    name = fields.Char(required=True)
    code = fields.Char(required=True)

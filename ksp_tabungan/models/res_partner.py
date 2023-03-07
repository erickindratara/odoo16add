from odoo import api, fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    tabungan_ids = fields.One2many(
        comodel_name="ksp.tabungan",
        inverse_name="partner_id",
        string="Rekening Tabungan",
        readonly=True
    )

from odoo import api, fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    simpanan_ids = fields.One2many(comodel_name="ksp.simpanan", inverse_name="partner_id", string="Simpanan")

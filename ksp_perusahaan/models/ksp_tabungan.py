from odoo import api, fields, models


class Tabungan(models.Model):
    _inherit = 'ksp.tabungan'

    saham_ids = fields.One2many(comodel_name="ksp.saham", inverse_name="tabungan_id",
                                string="Saham", required=False, readonly=True)
    saham_count = fields.Integer(compute='_compute_saham_count', string="Lembar Saham")
    saham_current_value = fields.Float(compute='_compute_saham_current_value', string="Nilai Saham Saat Ini")

    @api.depends('saham_ids')
    def _compute_saham_count(self):
        for me in self:
            me.update({
                'saham_count': len(me.saham_ids)
            })
        return

    @api.depends('saham_ids')
    def _compute_saham_current_value(self):
        for me in self:
            me.update({
                'saham_current_value': sum([x.current_value for x in self.saham_ids])
            })
        return

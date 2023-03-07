from odoo import api, fields, models


class DividenTabungan(models.Model):
    _name = 'ksp.dividen.saham'
    _rec_name = 'name'
    _description = 'Dividen Tabungan'
    _order = 'id desc'

    name = fields.Char(readonly=True)
    keuntungan_id = fields.Many2one(comodel_name="ksp.keuntungan", string="Keuntungan", required=True, readonly=True)
    tabungan_id = fields.Many2one(comodel_name="ksp.tabungan", string="Rekening Tabungan", required=True, readonly=True)
    saham_id = fields.Many2one(comodel_name="ksp.saham", string="Saham", required=True, )
    saham_value = fields.Float(required=True)
    amount_dividen = fields.Float(readonly=True)
    partner_tabungan_id = fields.Many2one(comodel_name="res.partner", related="tabungan_id.partner_id")
    umur_saham = fields.Integer(string="Umur Saham (bulan)")

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            val['name'] = self.env.ref('ksp_perusahaan.seq_dividen_tabungan').next_by_id()
        return super(DividenTabungan, self).create(vals)


class TabunganLine(models.Model):
    _inherit = 'ksp.tabungan.line'

    saham_dividen_ids = fields.Many2many(comodel_name="ksp.dividen.saham", string="Saham Dividen", )

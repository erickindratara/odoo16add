from odoo import api, fields, models


class DividenTabungan(models.Model):
    _name = 'ksp.dividen.saham'
    _rec_name = 'name'
    _description = 'Dividen Tabungan'
    _order = 'id desc'

    @api.depends('keuntungan_id.dividen_saham_ids') 
    def _compute_row_number(self):
        for i, line in enumerate(sorted(self.keuntungan_id.dividen_saham_ids, key=lambda r: r.id), start=1):
            line.row_number = i

    row_number = fields.Integer(string='No.', compute='_compute_row_number', store=True)
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

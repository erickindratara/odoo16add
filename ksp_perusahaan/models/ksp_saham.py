import datetime
from dateutil import relativedelta

from odoo import api, fields, models, _


class Saham(models.Model):
    _name = 'ksp.saham'
    _rec_name = 'name'
    _description = 'Saham'
    _order = 'id desc'

    name = fields.Char(readonly=True)
    origin_value = fields.Float(readonly=True)
    partner_id = fields.Many2one(comodel_name="res.partner", string="Owner", required=False, readonly=True)
    state = fields.Selection(selection=[
        ('new', 'New'),
        ('owned', 'Owned'),
        ('booked', 'Booked')
    ], default='new', readonly=True)
    current_value = fields.Float(compute='_compute_current_value')
    tabungan_id = fields.Many2one(comodel_name="ksp.tabungan", string="Tabungan", required=False, )
    buy_id = fields.Many2one(comodel_name="ksp.buy.saham", string="Booked in buy", required=False, )
    tanggal_pembelian_dihitung = fields.Date()
    saham_seri = fields.Char()

    def calculate_all_saham_current_value(self):
        all_saham = self.search([])
        all_saham_value = sum(x.current_value for x in all_saham)
        return all_saham_value

    def calculate_current_value(self):
        current_value = self.env['ksp.saham.value'].search([('saham_id', '=', self.id)], order='date_value desc', limit=1)
        return current_value.value

    def _compute_current_value(self):
        for rec in self:
            current_value = rec.calculate_current_value()
            rec.update({
                'current_value': current_value or rec.origin_value
            })
        return

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            val['name'] = "{}-{}".format(val['saham_seri'], self.env.ref('ksp_perusahaan.seq_saham').next_by_id())
            tgl_dihitung = datetime.datetime.now().replace(day=1)
            if tgl_dihitung.day > 15:
                tgl_dihitung += relativedelta.relativedelta(months=1)
            val['tanggal_pembelian_dihitung'] = tgl_dihitung

        return super(Saham, self).create(vals)

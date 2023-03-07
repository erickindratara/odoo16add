from odoo import api, fields, models


class Simpanan(models.Model):
    _name = 'ksp.simpanan'
    _rec_name = 'name'
    _description = 'Simpanan'
    _order = 'id desc'

    name = fields.Char(readonly=True)
    wajib_amount_per_month = fields.Float()
    saldo = fields.Float('Saldo', readonly=True)
    line_ids = fields.One2many(comodel_name="ksp.simpanan.line", inverse_name="simpanan_id", string="Line", readonly=True)
    partner_id = fields.Many2one(comodel_name="res.partner", string="Nasabah", required=True, )

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            val['name'] = self.env.ref('ksp_simpanan.seq_simpanan').next_by_id()
        return super(Simpanan, self).create(vals)

    def bayar_simpanan(self, amount):
        self.update({
            'saldo': self.saldo + amount,
            'line_ids': [(0, 0, {
                'amount_in': amount
            })]
        })
        return

    def tarik_simpanan(self, amount):
        self.update({
            'saldo': self.saldo - amount,
            'line_ids': [(0, 0, {
                'amount_out': amount
            })]
        })
        return

    def apply_fee_monthly(self):
        config_simpanan = self.env.ref('ksp_simpanan.default_config_simpanan')
        for me in self:
            fee_monthly = config_simpanan.fee_per_month_ids.filtered(lambda x: x.minimum_amount <= me.saldo)
            if not fee_monthly:
                continue
            fee_monthly = fee_monthly.sorted(lambda x: x.minimum_amount, reverse=True)[0]
            me.update({
                'saldo': me.saldo - fee_monthly.admin_fee_amount,
                'line_ids': [(0, 0, {
                    'amount_out': fee_monthly.admin_fee_amount,
                    'type_simpanan': 'admin'
                })]
            })
        return


class SimpananLine(models.Model):
    _name = 'ksp.simpanan.line'
    _rec_name = 'name'
    _description = 'Simpanan Line'

    name = fields.Char(readonly=True)
    transaction_date = fields.Date(default=fields.Date.today)
    amount_in = fields.Float()
    amount_out = fields.Float()
    simpanan_id = fields.Many2one(comodel_name="ksp.simpanan", string="Simpanan", required=True, )
    type_simpanan = fields.Selection(selection=[
        ('pokok', 'Pokok'),
        ('wajib', 'Wajib'),
        ('mutasi', 'Mutasi'),
        ('admin', 'Biaya admin'),
        ('dividen', 'Dividen')
    ], default='pokok', )

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            val['name'] = self.env.ref('ksp_simpanan.seq_simpanan_line').next_by_id()
        return super(SimpananLine, self).create(vals)

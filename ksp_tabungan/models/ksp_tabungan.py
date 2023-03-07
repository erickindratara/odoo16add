from odoo import api, fields, models


class Tabungan(models.Model):
    _name = 'ksp.tabungan'
    _rec_name = 'name'
    _description = 'Tabungan'
    _order = 'id desc'

    name = fields.Char(readonly=True, default='/', string="No Rekening")
    partner_id = fields.Many2one(comodel_name="res.partner", string="Customer", required=False, )
    line_ids = fields.One2many(comodel_name="ksp.tabungan.line", inverse_name="tabungan_id", string="Line",
                               required=False, )
    saldo = fields.Float('Saldo', readonly=True)
    state = fields.Selection(string="Status", selection=[
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
    ], default="draft", )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = self.env.ref('ksp_tabungan.seq_tabungan').next_by_id()
        return super().create(vals_list)

    def apply_fee_monthly(self):
        config_tabungan = self.env.ref('ksp_tabungan.default_config_tabungan')
        adm_type = self.env['ksp.tabungan.line.type'].search([('code', '=', 'ADM2')])
        for me in self:
            fee_monthly = config_tabungan.fee_per_month_ids.filtered(lambda x: x.minimum_amount <= me.saldo)
            if not fee_monthly:
                continue
            fee_monthly = fee_monthly.sorted(lambda x: x.minimum_amount, reverse=True)[0]
            me.update({
                'saldo': me.saldo - fee_monthly.admin_fee_amount,
                'line_ids': [(0, 0, {
                    'amount_out': fee_monthly.admin_fee_amount,
                    'type_id': adm_type.id
                })]
            })
        return


class TabunganLine(models.Model):
    _name = 'ksp.tabungan.line'
    _rec_name = 'name'
    _description = 'Tabungan Line'

    name = fields.Char(readonly=True, default='/')
    transaction_date = fields.Date(default=fields.Date.today)
    amount_in = fields.Float()
    amount_out = fields.Float()
    tabungan_id = fields.Many2one(comodel_name="ksp.tabungan", string="Tabungan", required=True, )
    type_id = fields.Many2one(comodel_name="ksp.tabungan.line.type", string="Type", required=True, )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = self.env.ref('ksp_tabungan.seq_tabungan_line').next_by_id()
        return super().create(vals_list)

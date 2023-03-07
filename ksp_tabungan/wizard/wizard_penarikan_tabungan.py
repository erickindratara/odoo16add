from odoo import api, fields, models


class WizardPanrikanTabungan(models.TransientModel):
    _name = 'wizard.penarikan.tabungan'
    _description = 'Wizard Penarikan Tabungan'

    partner_id = fields.Many2one(comodel_name="res.partner", string="Nasabah", required=True, )
    tabungan_id = fields.Many2one(comodel_name="ksp.tabungan", string="Rekening", required=True, )
    amount = fields.Monetary()
    currency_id = fields.Many2one(related="company_id.currency_id", string='Currency', readonly=False)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company.id)

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for rec in self:
            return {'domain': {'tabungan_id': [('partner_id', '=', rec.partner_id.id)]}}

    def execute_penarikan(self):
        line_type = self.env['ksp.tabungan.line.type'].search([('code', '=', 'TRKN')])
        self.tabungan_id.update({
            'saldo': self.tabungan_id.saldo - self.amount,
            'line_ids': [(0, 0, {
                'amount_out': self.amount,
                'type_id': line_type.id
            })]
        })

        # apply fee withdrawal
        config_tabungan = self.env.ref('ksp_tabungan.default_config_tabungan')
        fee_withdrawal = config_tabungan.fee_per_withdrawal_ids.filtered(lambda x: x.minimum_amount <= self.amount)
        if fee_withdrawal:
            fee_withdrawal = fee_withdrawal.sorted(lambda x: x.minimum_amount, reverse=True)[0]
            adm_type = self.env['ksp.tabungan.line.type'].search([('code', '=', 'ADM1')])
            self.tabungan_id.update({
                'saldo': self.tabungan_id.saldo - fee_withdrawal.admin_fee_amount,
                'line_ids': [(0, 0, {
                    'amount_out': fee_withdrawal.admin_fee_amount,
                    'type_id': adm_type.id
                })]
            })
        return

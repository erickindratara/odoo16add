from odoo import api, fields, models


class WizardPanrikanSimpanan(models.TransientModel):
    _name = 'wizard.penarikan.simpanan'
    _description = 'Wizard Penarikan Simpanan'

    partner_id = fields.Many2one(comodel_name="res.partner", string="Nasabah", required=True, )
    simpanan_id = fields.Many2one(comodel_name="ksp.simpanan", string="Rekening", required=True, )
    amount = fields.Monetary()
    currency_id = fields.Many2one(related="company_id.currency_id", string='Currency', readonly=False)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company.id)

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for rec in self:
            return {'domain': {'simpananid': [('partner_id', '=', rec.partner_id.id)]}}

    def execute_penarikan(self):
        self.simpanan_id.update({
            'saldo': self.simpanan_id.saldo - self.amount,
            'line_ids': [(0, 0, {
                'amount_out': self.amount,
                'type_simpanan': 'mutasi'
            })]
        })

        # apply fee withdrawal
        config_simpanan = self.env.ref('ksp_simpanan.default_config_simpanan')
        fee_withdrawal = config_simpanan.fee_per_withdrawal_ids.filtered(lambda x: x.minimum_amount <= self.amount)
        if fee_withdrawal:
            fee_withdrawal = fee_withdrawal.sorted(lambda x: x.minimum_amount, reverse=True)[0]
            self.simpanan_id.update({
                'saldo': self.simpanan_id.saldo - fee_withdrawal.admin_fee_amount,
                'line_ids': [(0, 0, {
                    'amount_out': fee_withdrawal.admin_fee_amount,
                    'type_simpanan': 'admin'
                })]
            })
        return

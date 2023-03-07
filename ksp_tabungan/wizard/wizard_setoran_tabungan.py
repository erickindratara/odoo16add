from odoo import api, fields, models


class WizardSetoranTabungan(models.TransientModel):
    _name = 'wizard.setoran.tabungan'
    _description = 'Wizard Setoran Tabungan'

    partner_id = fields.Many2one(comodel_name="res.partner", string="Nasabah", required=True, )
    tabungan_id = fields.Many2one(comodel_name="ksp.tabungan", string="Rekening", required=True, )
    amount = fields.Monetary()
    currency_id = fields.Many2one(related="company_id.currency_id", string='Currency', readonly=False)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company.id)

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for rec in self:
            return {'domain': {'tabungan_id': [('partner_id', '=', rec.partner_id.id)]}}

    def execute_setoran(self):
        line_type = self.env['ksp.tabungan.line.type'].search([('code', '=', 'STRN')])
        self.tabungan_id.update({
            'saldo': self.tabungan_id.saldo + self.amount,
            'line_ids': [(0, 0, {
                'amount_in': self.amount,
                'type_id': line_type.id
            })]
        })
        return

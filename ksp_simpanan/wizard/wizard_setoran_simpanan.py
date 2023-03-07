from odoo import api, fields, models


class WizardSetoranSimpanan(models.TransientModel):
    _name = 'wizard.setoran.simpanan'
    _description = 'Wizard Setoran Simpanan'

    partner_id = fields.Many2one(comodel_name="res.partner", string="Nasabah", required=True, )
    simpanan_id = fields.Many2one(comodel_name="ksp.simpanan", string="Rekening", required=True, )
    wajib_amount_per_month = fields.Float(related="simpanan_id.wajib_amount_per_month")
    amount = fields.Monetary()
    currency_id = fields.Many2one(related="company_id.currency_id", string='Currency', readonly=False)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company.id)
    type_simpanan = fields.Selection(selection=[
        ('pokok', 'Pokok'),
        ('wajib', 'Wajib'),
    ], default='pokok', )

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for rec in self:
            return {'domain': {'simpanan_id': [('partner_id', '=', rec.partner_id.id)]}}

    def execute_setoran(self):
        self.simpanan_id.update({
            'saldo': self.simpanan_id.saldo + self.amount,
            'line_ids': [(0, 0, {
                'amount_in': self.amount,
                'type_simpanan': self.type_simpanan
            })]
        })
        return

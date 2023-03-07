from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError


class BuySaham(models.Model):
    _name = 'ksp.buy.saham'
    _rec_name = 'name'
    _description = 'Buy Saham'
    _order = 'id desc'

    name = fields.Char(default="Draft", readonly=True)
    partner_id = fields.Many2one(comodel_name="res.partner", string="Nasabah", readonly=True, required=True,
                                 states={'draft': [('readonly', False)]})
    tabungan_id = fields.Many2one(comodel_name="ksp.tabungan", string="Tabungan Receiver", readonly=True, required=True,
                                 states={'draft': [('readonly', False)]})
    amount = fields.Integer(required=True, readonly=True, states={'draft': [('readonly', False)]})
    invoice_amount = fields.Float(readonly=True, store=True)
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('paid', 'Paid'),
        ('done', 'Done'),
        ('cancel', 'Cancel')
    ], default='draft', required=True, states={'draft': [('readonly', False)]})
    count_available_stock = fields.Integer(compute='_compute_count_available_stock')
    saham_ids = fields.One2many(comodel_name="ksp.saham", inverse_name="buy_id", string="Booked Saham", required=False, )

    @api.depends('partner_id')
    def _compute_count_available_stock(self):
        count = self.env['ksp.saham'].search_count([('state', 'in', ['new'])])
        self.update({
            'count_available_stock': count
        })
        return

    def action_confirm(self):
        if self.state != 'draft':
            raise UserError(_("Only draft can set to confirm"))
        # check stock is available
        if self.amount > self.count_available_stock:
            raise UserError(_("Not enough available stock"))
        # book stock
        available_saham = self.env['ksp.saham'].search([('state', 'in', ['new'])], limit=self.amount)
        for saham in self.web_progress_iter(available_saham, "Booking saham"):
            self.update({
                'saham_ids': [(4, saham.id)]
            })
            saham.update({
                'state': 'booked'
            })
        self.onchange_amount()
        self.update({
            'state': 'confirm'
        })
        return

    def action_paid(self):
        if self.state != 'confirm':
            raise UserError(_("Only confirm can set to paid"))
        self.update({
            'state': 'paid'
        })
        return

    def action_cancel(self):
        if self.state != 'confirm':
            raise UserError(_("Only confirm can set to cancel"))
        for saham in self.saham_ids:
            saham.update({
                'state': 'new'
            })
        self.update({
            'state': 'cancel'
        })
        return

    def action_done(self):
        if self.state != 'paid':
            raise UserError(_("Only paid can set to done"))
        for saham in self.web_progress_iter(self.saham_ids, "Transfer ownership"):
            saham.update({
                'partner_id': self.partner_id.id,
                'state': 'owned'
            })
            self.tabungan_id.update({
                'saham_ids': [(4, saham.id)]
            })
        self.update({
            'saham_ids': [(5, 0, 0)]
        })
        self.update({
            'state': 'done'
        })
        return

    def onchange_amount(self):
        for me in self:
            if me.state != 'draft':
                continue
            current_value = sum(x.current_value for x in me.saham_ids)
            me.update({
                'invoice_amount': current_value
            })
        return

    @api.model_create_multi
    def create(self, values):
        for value in values:
            value['name'] = self.env.ref('ksp_perusahaan.seq_saham_buy').next_by_id()
        return super(BuySaham, self).create(values)

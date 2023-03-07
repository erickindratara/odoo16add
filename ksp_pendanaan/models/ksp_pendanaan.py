from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError
from datetime import datetime
from dateutil import relativedelta


class Pendanaan(models.Model):
    _name = 'ksp.pendanaan'
    _inherit = ['mail.thread']
    _rec_name = 'name'
    _description = 'Pendanaan'
    _order = 'id desc'

    name = fields.Char(readonly=True, default='Draft')
    partner_id = fields.Many2one(comodel_name="res.partner", string="Nasabah", required=True, readonly=True,
                                 states={'draft': [('readonly', False)]})
    amount = fields.Float(required=True, readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('done', 'Done')
    ], default='draft', readonly=True, states={'draft': [('readonly', False)]}, tracking=3,)
    tenor = fields.Integer(string="Tenor (bulan)", readonly=True, states={'draft': [('readonly', False)]})
    cicilan_amount = fields.Float(readonly=True, states={'draft': [('readonly', False)]})
    bunga = fields.Float(compute='_compute_bunga', string="Bunga (%)")
    cicilan_ids = fields.One2many(comodel_name="ksp.cicilan", inverse_name="pendanaan_id", string="Cicilan",
                                  required=False, readonly=True)
    survey_state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='draft', readonly=True, tracking=3,)
    image_nasabah = fields.Image(tracking=3,)
    image_ktp = fields.Image(tracking=3,)
    image_ktp_nasabah = fields.Image(tracking=3,)
    image_domisili = fields.Image(tracking=3,)
    image_usaha_ids = fields.Many2many(
        comodel_name='ir.attachment',
        string="Image Usaha",
        tracking=3,
    )

    def action_survey_approve(self):
        if self.state != 'confirm' or self.survey_state != 'open':
            raise UserError(_("Only open survey can set to approve"))
        self.update({
            'survey_state': 'approved'
        })
        return

    def action_survey_reject(self):
        if self.state != 'confirm' or self.survey_state != 'open':
            raise UserError(_("Only open survey can set to reject"))
        self.update({
            'survey_state': 'rejected',
            'state': 'rejected'
        })
        return

    @api.depends('amount', 'tenor', 'cicilan_amount')
    def _compute_bunga(self):
        for rec in self:
            bunga = 0
            if all([
                rec.amount,
                rec.tenor,
                rec.cicilan_amount
            ]):
                pokok = self.amount / self.tenor
                bunga = (self.cicilan_amount - pokok) / pokok * 100
            rec.update({
                'bunga': bunga
            })
        return

    @api.model_create_multi
    def create(self, values):
        for value in values:
            value['name'] = self.env.ref('ksp_pendanaan.seq_pendanaan').next_by_id()
        return super(Pendanaan, self).create(values)

    def action_confirm(self):
        if self.state != 'draft':
            raise UserError(_("Only draft can set to confirm"))
        self.update({
            'state': 'confirm',
            'survey_state': 'open'
        })
        return

    def action_rejected(self):
        if self.state != 'confirm':
            raise UserError(_("Only confirmed can set to rejected"))
        if self.survey_state != 'approved':
            raise UserError(_("Only survey approved can set to be rejected"))
        self.update({
            'state': 'rejected'
        })
        return

    def action_approved(self):
        if self.state != 'confirm':
            raise UserError(_("Only confirmed can set to approved"))
        if self.survey_state != 'approved':
            raise UserError(_("Only survey approved can set to be approved"))
        # generate cicilan here
        for i in self.web_progress_iter(range(self.tenor), "Generating cicilan"):
            self.env['ksp.cicilan'].create({
                'pendanaan_id': self.id,
                'partner_id': self.partner_id.id,
                'amount': self.cicilan_amount,
                'cicilan_index': i + 1,
                'due_date': datetime.now() + relativedelta.relativedelta(months=i + 1)
            })
        self.update({
            'state': 'approved'
        })
        return

    def action_done(self):
        if self.state != 'approved':
            raise UserError(_("Only approved can set to done"))
        self.update({
            'state': 'done'
        })
        return

from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError


class Cicilan(models.Model):
    _name = 'ksp.cicilan'
    _rec_name = 'name'
    _description = 'Cicilan'

    name = fields.Char(readonly=True)
    pendanaan_id = fields.Many2one(comodel_name="ksp.pendanaan", string="Pendanaan", required=True, )
    partner_id = fields.Many2one(comodel_name="res.partner", string="Nasabah", required=True, )
    amount = fields.Float()
    cicilan_index = fields.Integer()
    due_date = fields.Date()
    state = fields.Selection(selection=[
        ('open', 'Open'),
        ('closed', 'Closed'),
    ], default='open', )

    def action_close(self):
        if self.state != 'open':
            raise UserError(_("Cannot close cicilan that is not open"))
        self.update({
            'state': 'closed'
        })
        return

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            val['name'] = self.env.ref('ksp_pendanaan.seq_cicilan').next_by_id()
        return super(Cicilan, self).create(vals_list)

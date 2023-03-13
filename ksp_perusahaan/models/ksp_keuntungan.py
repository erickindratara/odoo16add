from odoo import api, fields, models
from datetime import datetime
from dateutil import relativedelta


class Keuntungan(models.Model):
    _name = 'ksp.keuntungan'
    _rec_name = 'name'
    _description = 'Keuntungan'
    _order = 'id desc'


    name = fields.Char(readonly=True)
    tahun = fields.Char(readonly=True, required=True, states={'draft': [('readonly', False)]})
    amount = fields.Float(readonly=True, required=True, states={'draft': [('readonly', False)]})
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancel')
    ], default="draft", readonly=True, required=True, states={'draft': [('readonly', False)]})
    persen_bagi_hasil = fields.Float(string="Persen bagi hasil (%)", readonly=True, required=True, states={'draft': [('readonly', False)]})
    dana_dpk = fields.Float(readonly=True, string="Total DPK")
    dividen_saham_ids = fields.One2many(comodel_name="ksp.dividen.saham", inverse_name="keuntungan_id",
                                           string="Dividen Saham", readonly=True, )
 
        
    def generate_dividen_saham(self):
        # Get all the saham data from the database
        all_saham = self.env['ksp.saham'].search([])
        
        # Create an empty dictionary to store the calculated saham values
        saham_values = {}
        
        # Create a set to store the unique tabungan IDs
        tabungan_ids = set()
        
        # Loop through all the saham data
        for saham in all_saham:
            # If the saham is associated with a tabungan account
            if saham.tabungan_id.id:
                # Add the tabungan ID to the set of unique tabungan IDs
                tabungan_ids.add(saham.tabungan_id.id)
                
                # Calculate the age of the saham in months
                akhir_tahun = datetime.strptime(f"{self.tahun}-12-31", "%Y-%m-%d")
                delta = relativedelta.relativedelta(akhir_tahun, saham.tanggal_pembelian_dihitung)
                umur = delta.months
                if delta.days:
                    umur += 1
                    
                # Calculate the value of the saham based on its age
                saham_value = saham.current_value if umur >= 12 else (umur / 12) * saham.current_value
                
                # Store the saham value and age in the saham_values dictionary
                saham_values[saham.id] = {'saham_value': saham_value, 'umur': umur}
        
        # Calculate the total value of all the saham in the database
        dana_dpk = self.env['ksp.saham'].calculate_all_saham_current_value()
        
        # Calculate the dividend amount for each saham and store it in a list
        amount_dividens = [
            (
                self.amount * (saham_values[saham.id]['saham_value'] / dana_dpk) * (self.persen_bagi_hasil / 100),
                saham.tabungan_id.id,
                saham_values[saham.id]['saham_value'],
                saham_values[saham.id]['umur'],
                saham.id
            )
            for saham in all_saham if saham.tabungan_id.id in tabungan_ids
        ]
        
        # Create a new dividen saham record for each tabungan account and saham
        self.env['ksp.dividen.saham'].create([
            {
                'keuntungan_id': self.id,
                'tabungan_id': tabungan_id,
                'saham_value': saham_value,
                'amount_dividen': amount_dividen,
                'umur_saham': umur,
                'saham_id': saham_id
            }
            for amount_dividen, tabungan_id, saham_value, umur, saham_id in amount_dividens
        ])
        
        # Update the dana_dpk field in the current record
        self.update({'dana_dpk': dana_dpk})

    def set_done(self):
        dividen_group = self.env['ksp.dividen.saham'].read_group([('keuntungan_id', '=', self.id)], [], 'tabungan_id')
        for dividen in dividen_group:
            obj_dividen = self.env['ksp.dividen.saham'].search(dividen['__domain'])
            type_tabungan = self.env['ksp.tabungan.line.type'].search([('code', '=', 'DIVS')])
            tabungan = self.env['ksp.tabungan'].browse(dividen['tabungan_id'][0])
            self.env['ksp.tabungan.line'].create({
                'amount_in': dividen['amount_dividen'],
                'tabungan_id': tabungan.id,
                'type_id': type_tabungan.id,
                'saham_dividen_ids': [(6, 0, obj_dividen.ids)]
            })
            tabungan.update({
                'saldo': tabungan.saldo + dividen['amount_dividen']
            })
            pass
        self.update({
            'state': 'done'
        })
        return

    def set_cancel(self):
        self.update({
            'state': 'cancel'
        })
        return

    def set_confirm(self):
        self.generate_dividen_saham()
        self.update({
            'state': 'confirm'
        })
        return

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            val['name'] = self.env.ref('ksp_perusahaan.seq_keuntungan').next_by_id()
        return super(Keuntungan, self).create(vals)

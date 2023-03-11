from odoo import api, fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    tabungan_ids = fields.One2many(
        comodel_name="ksp.tabungan",
        inverse_name="partner_id",
        string="Rekening Tabungan",
        readonly=True
    ) 
    is_nasabah = fields.Boolean(string="nasabah", default=True) 
 
    def cekdefaultfilter(self):  
        ir_filters = self.env['ir.filters'].sudo(); ir_filters.search([('model_id', '=', 'res.partner')]).sudo().unlink()  
        ir_filters.sudo().create({ 
            'model_id'  : 'res.partner' ,'name'      : "nasabah only"   ,
            'active'    : 'True'          ,'domain'    : '[["is_nasabah","=",True]]'  ,
            # 'active'    : 'True'          ,'domain'    : '[["stage","in",("NEW","DRF")]]'  ,
            # 'sort'      : "[]"            ,'context'   : "{'group_by': ['customerid','senddate:week']}",
            'sort'      : "[]",
            'is_default': 'True',})
                 
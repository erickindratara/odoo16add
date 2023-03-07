from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError


class Partner(models.Model):
    _inherit = 'res.partner'

    pendanaan_ids = fields.One2many(comodel_name="ksp.pendanaan", inverse_name="partner_id", string="Pendanaan", required=False, readonly=True)
    cicilan_ids = fields.One2many(comodel_name="ksp.cicilan", inverse_name="partner_id", string="Cicilan", required=False, readonly=True)

    @api.model
    def hide_menu_discuss(self):
        menus = [
            'mail.menu_root_discuss'
        ]
        for menu in menus:
            try:
                obj = self.env.ref(menu)
                obj.update({
                    'active': False
                })
            except:
                pass
        return
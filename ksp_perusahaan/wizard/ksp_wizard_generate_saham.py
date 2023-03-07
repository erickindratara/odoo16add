from odoo import api, fields, models, _
from odoo.exceptions import UserError


class WizardGenerateSaham(models.TransientModel):
    _name = 'ksp.wizard.generate.saham'
    _description = 'Wizard Generate Saham'

    value = fields.Float()
    amount = fields.Integer()
    saham_seri = fields.Char()

    def exec_generate_saham(self):
        if len(self.saham_seri) < 2:
            raise UserError(_("Saham seri at least 2 characters"))
        for i in self.web_progress_iter(range(self.amount), msg="Generating saham"):
            self.env['ksp.saham'].create({
                'origin_value': self.value,
                'saham_seri': self.saham_seri
            })
        return

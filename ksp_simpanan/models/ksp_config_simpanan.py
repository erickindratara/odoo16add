from odoo import api, fields, models


class ConfigSimpananFeePerMonth(models.Model):
    _name = 'ksp.config.simpanan.fee.per.month'
    _description = 'Config Simpanan Fee Per Month'
    _order = 'sequence, id'

    sequence = fields.Integer(default=10)
    minimum_amount = fields.Float()
    admin_fee_amount = fields.Float()
    config_id = fields.Many2one(comodel_name="ksp.config.simpanan", string="Config", required=False, )


class ConfigSimpananFeePerWithdrawal(models.Model):
    _name = 'ksp.config.simpanan.fee.per.withdrawal'
    _description = 'Config Simpanan Fee Per Withdrawal'
    _order = 'sequence, id'

    sequence = fields.Integer(default=10)
    minimum_amount = fields.Float()
    admin_fee_amount = fields.Float()
    config_id = fields.Many2one(comodel_name="ksp.config.simpanan", string="Config", required=False, )


class ConfigSimpanan(models.Model):
    _name = 'ksp.config.simpanan'
    _description = 'Config Simpanan'

    name = fields.Char(readonly=True)
    fee_per_month_ids = fields.One2many(comodel_name="ksp.config.simpanan.fee.per.month", inverse_name="config_id",
                                        string="Fee Per Month", required=False, )
    fee_per_withdrawal_ids = fields.One2many(comodel_name="ksp.config.simpanan.fee.per.withdrawal",
                                             inverse_name="config_id",
                                             string="Fee Per Month", required=False, )

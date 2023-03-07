from odoo import api, fields, models


class ConfigTabunganFeePerMonth(models.Model):
    _name = 'ksp.config.tabungan.fee.per.month'
    _description = 'Config Tabungan Fee Per Month'
    _order = 'sequence, id'

    sequence = fields.Integer(default=10)
    minimum_amount = fields.Float()
    admin_fee_amount = fields.Float()
    config_id = fields.Many2one(comodel_name="ksp.config.tabungan", string="Config", required=False, )


class ConfigTabunganFeePerWithdrawal(models.Model):
    _name = 'ksp.config.tabungan.fee.per.withdrawal'
    _description = 'Config Tabungan Fee Per Withdrawal'
    _order = 'sequence, id'

    sequence = fields.Integer(default=10)
    minimum_amount = fields.Float()
    admin_fee_amount = fields.Float()
    config_id = fields.Many2one(comodel_name="ksp.config.tabungan", string="Config", required=False, )


class ConfigTabungan(models.Model):
    _name = 'ksp.config.tabungan'
    _description = 'Config Tabungan'

    name = fields.Char(readonly=True)
    fee_per_month_ids = fields.One2many(comodel_name="ksp.config.tabungan.fee.per.month", inverse_name="config_id",
                                        string="Fee Per Month", required=False, )
    fee_per_withdrawal_ids = fields.One2many(comodel_name="ksp.config.tabungan.fee.per.withdrawal",
                                             inverse_name="config_id",
                                             string="Fee Per Month", required=False, )

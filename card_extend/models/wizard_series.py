from odoo import api, fields, models, _
from odoo.exceptions import UserError


class WizardSeries(models.Model):
    _name = 'wizard.series'
    _description = '万智牌系列'

    name = fields.Char(string='系列名称')

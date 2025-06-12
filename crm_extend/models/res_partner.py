# -*- coding: utf-8 -*-
import re
import logging
import datetime
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.api import NewId
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)

GENDER = [
    ('male', '男'),
    ('female', '女')
]


class ResPartner(models.Model):
    _inherit = "res.partner"

    identity_id = fields.Char(string='身份证号')
    age = fields.Integer(string='年龄', compute='_compute_information')
    gender = fields.Selection(selection=GENDER, string='性别', compute='_compute_information')
    title = fields.Many2one(comodel_name='res.partner.title', compute='_compute_information')

    @api.depends('identity_id')
    def _compute_information(self):
        for record in self:
            if identity_number := record.identity_id:
                record.gender = record._compute_gender(identity_number)
                record.age = record._compute_age(identity_number)
                record.title = record._compute_title(record.gender)
            else:
                record.gender, record.age, record.title = None, 0, None

    def _compute_age(self, identity_number) -> int:
        try:
            birth_date = datetime.datetime.strptime(identity_number[6:14], "%Y%m%d")
            today = datetime.date.today()
            age = relativedelta(today, birth_date).years
            return age
        except Exception as e:
            _logger.error(e)

    def _compute_gender(self, identity_number) -> str:
        if int(identity_number[-2]) % 2:
            return 'male'
        return 'female'

    def _compute_title(self, gender) -> [NewId | int]:
        match gender:
            case 'male':
                title = self.env['res.partner.title'].with_context({'lang': 'en_US'}).search([('name', '=', 'Mister')], limit=1)
                return title.id
            case 'female':
                title = self.env['res.partner.title'].with_context({'lang': 'en_US'}).search([('name', '=', 'Miss')], limit=1)
                return title.id
            case _:
                return None

    @api.constrains('identity_id')
    def _check_information(self):
        for record in self:
            identity_number = record.identity_id
            pattern = r'^[1-9][0-9]{16}[0-9Xx]'
            try:
                if re.search(pattern, identity_number):
                    pass
            except Exception as e:
                _logger.error(e)

    def action_batch_import_customer(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _("批量导入"),
            'res_model': 'customer.import.wizard',
            'target': 'new',
            'views': [(self.env.ref('crm_extend.customer_import_wizard_form').id, 'form')],
        }

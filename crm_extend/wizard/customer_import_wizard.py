import logging

from odoo import api, fields, models, _
from odoo.exceptions import UserError

from .utils import operations

_logger = logging.getLogger(__name__)


class CustomerImportWizard(models.TransientModel):
    _name = 'customer.import.wizard'
    _description = 'Batch import customer information excel'

    directory_path = fields.Char(string='文件夹路径')

    def import_customer_data(self):
        records, failure = operations.call_point(self.directory_path)
        for record in records:
            if not self.env['res.partner'].search([('identity_id', '=', record.get('identity_id'))]):
                self.env['res.partner'].create(record)


import io
import base64
import logging

from odoo import api, fields, models, _

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

        if failure:
            output = io.StringIO()
            output.write("失败详情\n")
            for f in failure:
                output.write(f"{f}\n")
            file_data = base64.b64encode(output.getvalue().encode())

            attachment = self.env['ir.attachment'].create({
                'name': '客户导入失败日志.txt',
                'type': 'binary',
                'datas': file_data,
                'res_model': 'res.users',
                'res_id': self.env.uid,
            })

            # 返回下载动作
            return {
                'type': 'ir.actions.act_url',
                'url': f'/web/content/{attachment.id}?download=true',
                'target': 'self',
            }

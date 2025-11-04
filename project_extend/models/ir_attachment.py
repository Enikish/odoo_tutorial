from odoo import models, fields, api, _
from odoo.api import ValuesType, Self
from odoo.exceptions import UserError


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    def check_attachment_deletable(self):
        self.ensure_one()
        if hasattr(self.env[self.res_model], 'check_attachment_writable'):
            return self.env[self.res_model].browse(self.res_id).check_attachment_writable()
        return True

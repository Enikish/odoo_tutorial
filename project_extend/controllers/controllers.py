# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.addons.mail.controllers.attachment import AttachmentController
from odoo.exceptions import AccessError
from odoo.http import request


class MyAttachmentController(AttachmentController):
    def mail_attachment_upload(self, ufile, thread_id, thread_model, is_pending=False, **kwargs):
        env = http.request.env
        # 👇 确保整条权限检查在 sudo 环境中执行
        model = env[thread_model].sudo()

        if hasattr(model, 'check_attachment_writable'):
            record = model.browse(int(thread_id))
            if not record.exists():
                # ✅ 直接返回 JSON 响应，状态码 200
                return request.make_json_response({"error": _("Record not found or deleted.")})
            if not record.check_attachment_writable():
                # ✅ 不 raise，让前端收到 {error: "..."}，界面会正常显示错误提示
                return request.make_json_response({"error": _("You are not allowed to upload attachments.")})

            # 通过检查后继续调用父类逻辑
        return super().mail_attachment_upload(ufile, thread_id, thread_model, is_pending, **kwargs)

    def mail_attachment_delete(self, attachment_id, access_token=None, **kwargs):
        attachment = request.env["ir.attachment"].browse(int(attachment_id)).exists()
        if not attachment.check_attachment_deletable():
            raise AccessError(_("Record cannot be deleted."))
        res = super().mail_attachment_delete(attachment_id, access_token, **kwargs)
        return res

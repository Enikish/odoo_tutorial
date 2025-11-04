# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from markupsafe import Markup


class ProjectProject(models.Model):
    _inherit = "project.project"

    state = fields.Selection(selection=[('draft', 'Draft'),
                                        ('pending', 'pending'),
                                        ('approved', 'Approved'),
                                        ('rejected', 'Rejected')], string="Status", default="draft")

    def button_validation_apply(self):
        self.ensure_one()
        self.write({'state': 'pending'})
        return True

    def button_approved(self):
        self.ensure_one()
        self.write({'state': 'approved'})
        return True

    def button_rejected(self):
        self.ensure_one()
        self.write({'state': 'rejected'})
        return True

    def button_reset_draft(self):
        self.ensure_one()
        self.write({'state': 'draft'})
        return True

    def action_subscribe(self):
        subscribe = "message_subscribe"
        post = "message_post"
        # 获取下标类型
        subtype_record = self.env.ref('project_extend.project_subscribe', raise_if_not_found=False)
        if not subtype_record:
            return False

        # 订阅项目变更
        getattr(self, subscribe)(
            partner_ids=(1, 2, 6),
            subtype_ids=subtype_record.ids
        )

        # 发送消息 - 注意 subtype_xmlid 需要传递字符串，不是列表
        getattr(self, post)(
            subtype_xmlid='project_extend.project_subscribe',
            body=self.env._("Hello World")
        )

        # 在项目右上角聊天面板显示通知消息（类似 tier_validation）
        self.message_post(
            body=Markup(
                "<p><b>项目订阅已启用</b></p>"
                "<ul>"
                "<li>订阅人员：管理员、项目经理、项目成员</li>"
                "<li>消息类型：项目变更通知</li>"
                "<li>状态：已激活</li>"
                "</ul>"
            ),
            message_type="notification",
            subtype_xmlid="mail.mt_note",
        )

        # 发送邮件给订阅用户
        self._send_subscription_email()

        return True

    def _send_subscription_email(self):
        """发送邮件给订阅用户"""
        # 获取订阅的用户（partner_ids: 1, 2, 6）
        partners = self.env['res.partner'].browse([3, 7])

        email_values = {
            'subject': _("[项目通知] 项目 %s 已启用订阅功能") % self.name,
            'email_from': self.env.user.email or self.env.company.email,
            'body_html': self._get_email_body(),
            'auto_delete': True,
        }

        mail_obj = self.env['mail.mail']

        # 为每个有邮箱的联系人发送邮件
        for partner in partners:
            if partner.email:
                email_values['email_to'] = partner.email
                mail = mail_obj.create(email_values)
                try:
                    mail.send()
                except Exception as e:
                    # 邮件发送失败时，在项目消息中记录
                    self.message_post(
                        body=_("邮件发送失败: %s") % str(e),
                        message_type="notification",
                        subtype_xmlid="mail.mt_note",
                    )

        return True

    def _get_email_body(self):
        """生成邮件内容"""
        return Markup(
            "<html>"
            "<body>"
            "<p>亲爱的团队成员,</p>"
            "<p>项目 <b>%s</b> 已启用订阅功能,您将收到该项目的所有更新通知。</p>"
            "<p><b>项目信息:</b></p>"
            "<ul>"
            "<li>项目名称: %s</li>"
            "<li>项目编号: %s</li>"
            "<li>启用时间: %s</li>"
            "</ul>"
            "<p>如有任何问题,请通过Odoo内部消息与我们联系。</p>"
            "<p>最佳问候,<br/>Odoo 项目管理系统</p>"
            "</body>"
            "</html>"
        ) % (
            self.name,
            self.name,
            self.name,
            fields.Datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

    def check_attachment_writable(self) -> bool:
        return self.state not in ('pending', 'approved', 'rejected')


class ProjectTask(models.Model):
    _inherit = "project.task"

    def check_status(self):
        return

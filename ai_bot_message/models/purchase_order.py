from odoo import models, api, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def action_send_odoo_bot_message(self):
        for order in self:
            # 查找 OdooBot 用户
            bot_user = self.env.ref('base.partner_root', raise_if_not_found=False)
            if not bot_user:
                # 如果找不到，尝试查找第一个系统用户
                bot_user = self.env['res.partner'].sudo().search([('id', '=', 2)], limit=1)
            
            if not bot_user:
                raise UserError(_("OdooBot user not found."))

            current_user = self.env.user
            current_partner = current_user.partner_id
            
            message_body = _("你好 %s，这是一条来自 OdooBot 的自动消息。\n采购单：%s") % (
                current_user.name, order.name
            )

            # 查找是否已有私聊频道
            channel = self.env['discuss.channel'].sudo().search([
                ('channel_type', '=', 'chat'),
                ('channel_partner_ids', 'in', [current_partner.id, bot_user.id]),
            ], limit=1)
            
            # 进一步验证频道是否包含两个成员
            if channel:
                partner_ids = channel.channel_partner_ids.ids
                if not (current_partner.id in partner_ids and bot_user.id in partner_ids):
                    channel = False

            # 没有则创建
            if not channel:
                channel = self.env['discuss.channel'].sudo().create({
                    'name': f"OdooBot, {current_user.name}",
                    'channel_type': 'chat',
                    'channel_partner_ids': [(4, current_partner.id), (4, bot_user.id)],
                })

            # 发消息
            channel.sudo().message_post(
                body=message_body,
                author_id=bot_user.id,
                message_type="comment",
                subtype_xmlid="mail.mt_comment",
            )

        return {
            'type': 'ir.actions.client',
            'tag': 'action_open_bot_chat',
            'params': {
                'channel_id': channel.id,
            }
        }

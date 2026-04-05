/** @odoo-module **/

import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";

function openBotChatAction(env, action) {
    const channelId = action.params?.channel_id;
    if (!channelId) {
        console.error("Channel ID is missing");
        return;
    }

    // 使用 messaging service 打开聊天窗口
    const messaging = env.services.messaging;
    if (messaging && messaging.openChat) {
        messaging.openChat({ channelId: channelId });
    } else {
        // 降级方案：直接打开讨论频道
        return env.services.action.doAction({
            type: "ir.actions.act_window",
            res_model: "discuss.channel",
            views: [[false, "form"]],
            res_id: channelId,
            target: "current",
        });
    }
}

registry.category("actions").add("action_open_bot_chat", openBotChatAction);

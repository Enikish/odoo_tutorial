# -*- coding: utf-8 -*-
# from odoo import http


# class AiBotMessage(http.Controller):
#     @http.route('/ai_bot_message/ai_bot_message', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ai_bot_message/ai_bot_message/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ai_bot_message.listing', {
#             'root': '/ai_bot_message/ai_bot_message',
#             'objects': http.request.env['ai_bot_message.ai_bot_message'].search([]),
#         })

#     @http.route('/ai_bot_message/ai_bot_message/objects/<model("ai_bot_message.ai_bot_message"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ai_bot_message.object', {
#             'object': obj
#         })


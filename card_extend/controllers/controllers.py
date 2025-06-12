# -*- coding: utf-8 -*-
# from odoo import http


# class ./customAddons/cardExtend(http.Controller):
#     @http.route('/./custom_addons/card_extend/./custom_addons/card_extend', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/./custom_addons/card_extend/./custom_addons/card_extend/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('./custom_addons/card_extend.listing', {
#             'root': '/./custom_addons/card_extend/./custom_addons/card_extend',
#             'objects': http.request.env['./custom_addons/card_extend../custom_addons/card_extend'].search([]),
#         })

#     @http.route('/./custom_addons/card_extend/./custom_addons/card_extend/objects/<model("./custom_addons/card_extend../custom_addons/card_extend"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('./custom_addons/card_extend.object', {
#             'object': obj
#         })


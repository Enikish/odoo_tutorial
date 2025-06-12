# -*- coding: utf-8 -*-
# from odoo import http


# class .\customAddons\crmExtend(http.Controller):
#     @http.route('/.\custom_addons\crm_extend/.\custom_addons\crm_extend', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/.\custom_addons\crm_extend/.\custom_addons\crm_extend/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('.\custom_addons\crm_extend.listing', {
#             'root': '/.\custom_addons\crm_extend/.\custom_addons\crm_extend',
#             'objects': http.request.env['.\custom_addons\crm_extend..\custom_addons\crm_extend'].search([]),
#         })

#     @http.route('/.\custom_addons\crm_extend/.\custom_addons\crm_extend/objects/<model(".\custom_addons\crm_extend..\custom_addons\crm_extend"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('.\custom_addons\crm_extend.object', {
#             'object': obj
#         })


# -*- coding: utf-8 -*-
# from odoo import http


# class ProjectExtend(http.Controller):
#     @http.route('/project_extend/project_extend', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project_extend/project_extend/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('project_extend.listing', {
#             'root': '/project_extend/project_extend',
#             'objects': http.request.env['project_extend.project_extend'].search([]),
#         })

#     @http.route('/project_extend/project_extend/objects/<model("project_extend.project_extend"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project_extend.object', {
#             'object': obj
#         })


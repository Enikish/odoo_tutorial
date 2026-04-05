# -*- coding: utf-8 -*-
# from odoo import http


# class ProjectTierValidation(http.Controller):
#     @http.route('/project_tier_validation/project_tier_validation', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project_tier_validation/project_tier_validation/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('project_tier_validation.listing', {
#             'root': '/project_tier_validation/project_tier_validation',
#             'objects': http.request.env['project_tier_validation.project_tier_validation'].search([]),
#         })

#     @http.route('/project_tier_validation/project_tier_validation/objects/<model("project_tier_validation.project_tier_validation"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project_tier_validation.object', {
#             'object': obj
#         })


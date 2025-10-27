from odoo import models, fields, api


class ProjectProject(models.Model):
    _name = 'project.project'
    _inherit = ["project.project", "tier.validation"]
    _state_from = ["draft", "pending"]
    _state_to = ["approved"]
    _tier_validation_manual_config = False

    @api.model
    def _get_under_validation_exceptions(self):
        res = super()._get_under_validation_exceptions()
        res.append("route_id")
        return res

    def request_validation(self):
        res = super().request_validation()
        self.button_validation_apply()
        return res

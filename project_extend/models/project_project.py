# -*- coding: utf-8 -*-

from odoo import models, fields, api


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

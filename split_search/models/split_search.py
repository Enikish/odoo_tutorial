# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SplitSearch(models.AbstractModel):
    _name = 'split.search'

    def _prepare_domain(self, domain):
        domain = domain or []
        if isinstance(domain, (list, tuple)):
            return self._split_domain(domain)
        return domain

    @api.model
    def _split_domain(self, domain):
        split_sign = self.env['ir.config_parameter'].sudo().get_param('split_search.split_sign', None)
        new_domain = []
        for cond in domain:
            if isinstance(cond, (list, tuple)) and len(cond) >= 3:
                field, operator, value = cond[0], cond[1], cond[2]
                if isinstance(value, str) and split_sign in value and operator in ('ilike', 'like', '=', 'in', '=ilike'):
                    parts = [v.strip() for v in value.split(split_sign) if v.strip()]
                    if len(parts) > 1:
                        or_domain = []
                        for index, part in enumerate(parts):
                            if index > 0:
                                or_domain.insert(0, '|')
                            or_domain.append((field, operator, part))
                        new_domain += or_domain
                        continue
            new_domain.append(cond)
        return new_domain

    def search_fetch(self, domain, field_names, offset=0, limit=None, order=None):
        domain = self._prepare_domain(domain)
        res = super().search_fetch(domain, field_names, offset, limit, order)
        return res

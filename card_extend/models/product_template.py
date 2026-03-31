import logging
from odoo import models, api, fields, _


_logger = logging.getLogger(__name__)
CARD_TYPE = [
    ('sole', '单卡'),
    ('pack', '卡包'),
]


class ProductTemplate(models.Model):
    _inherit = "product.template"

    card_series = fields.Many2one(comodel_name='wizard.series', string='系列')
    card_type = fields.Selection(selection=CARD_TYPE, string='牌类',
                                 help='该选项为区分产品是否为单卡, 例如: "三重大师艾莎","铁木尔之吼艾丝琦"',
                                 default='pack')

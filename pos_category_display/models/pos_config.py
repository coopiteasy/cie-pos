from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    pos_category_display = fields.Selection(
        [("full", "Full"), ("minimized", "Minimized")],
        string="POS Category Display",
        default="full",
    )

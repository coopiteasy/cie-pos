from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    pos_category_display_setting = fields.Selection(
        [("full", "Full"), ("minimized", "Minimized")],
        string="POS Category Display",
        default="full",
        config_parameter="point_of_sale.pos_category_display_setting",
    )

    @api.onchange("pos_category_display_setting")
    def _onchange_pos_category_display_setting(self):
        self.env["pos.config"].search([]).write(
            {"pos_category_display": self.pos_category_display_setting}
        )

# SPDX-FileCopyrightText: 2025 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import models


class PosSession(models.Model):
    _inherit = "pos.session"

    def _loader_params_product_product(self):
        res = super()._loader_params_product_product()
        res["search_params"]["fields"] += [
            "display_weight",
            "display_unit",
            "main_seller_id",
        ]
        return res

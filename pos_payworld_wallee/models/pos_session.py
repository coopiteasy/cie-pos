# SPDX-FileCopyrightText: 2026 Vincent Haulotte
# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import models


class PosSession(models.Model):
    _inherit = "pos.session"

    def _loader_params_pos_payment_method(self):
        result = super()._loader_params_pos_payment_method()
        fields = result["search_params"]["fields"]
        for field_name in (
            "wallee_terminal_identifier",
            "wallee_space_id",
            "wallee_language",
        ):
            if field_name not in fields:
                fields.append(field_name)
        return result

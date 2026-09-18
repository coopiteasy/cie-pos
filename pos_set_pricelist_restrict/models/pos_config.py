# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    restrict_pricelist_control = fields.Boolean(
        string="Restrict Pricelist to Managers",
        help="Only users with Manager access rights for PoS app can change the pricelist.",
    )

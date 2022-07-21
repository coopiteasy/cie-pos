# SPDX-FileCopyrightText: 2022 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    created_from_pos = fields.Boolean(
        string="Created from Point of Sale?", compute="_compute_created_from_pos"
    )

    def _compute_created_from_pos(self):
        for invoice in self:
            invoice.created_from_pos = bool(
                self.env["pos.order"].search([("name", "=", invoice.origin)])
            )

# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import models


class PosSession(models.Model):
    _inherit = "pos.session"

    def action_pos_session_open(self):
        res = super().action_pos_session_open()
        for session in self:
            if session.state == "opening_control" and session.config_id.cash_control:
                session.state = "opened"
        return res

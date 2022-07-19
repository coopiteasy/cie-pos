# Copyright 2016 Robin Keunen, Coop IT Easy SC
# Copyright 2020 Houssine Bakkali, Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    cash_rounding = fields.Boolean(string="Cash Rounding Journal", default=False)

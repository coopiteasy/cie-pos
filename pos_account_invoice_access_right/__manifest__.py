# Copyright 2020 Coop IT Easy SCRL fs
#   Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "POS Invoice Access Right",
    "version": "12.0.1.0.0",
    "depends": ["account", "point_of_sale"],
    "author": "Coop IT Easy SC",
    "license": "AGPL-3",
    "category": "Point Of Sale",
    "website": "https://www.coopiteasy.be",
    "summary": """
        Allows read access on `account.invoice` to `point_of_sale.group_pos_user`
    """,
    "data": ["security/ir.model.access.csv"],
    "installable": True,
}

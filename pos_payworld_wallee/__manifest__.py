# SPDX-FileCopyrightText: 2026 Vincent Haulotte
# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "POS Payworld / Wallee Terminal",
    "summary": "Integrate Odoo POS with Payworld/Wallee cloud payment terminals",
    "version": "16.0.1.0.1",
    "depends": [
        "point_of_sale",
    ],
    "author": "Vincent Haulotte, Coop IT Easy SC",
    "category": "Sales/Point of Sale",
    "website": "https://github.com/coopiteasy/cie-pos",
    "data": [
        "views/pos_payment_method_views.xml",
    ],
    "assets": {
        "point_of_sale.assets": [
            "pos_payworld_wallee/static/src/js/**/*",
        ],
    },
    "license": "AGPL-3",
}

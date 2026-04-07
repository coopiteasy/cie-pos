# SPDX-FileCopyrightText: 2022 Coop IT Easy SCRLfs
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Generate POS receipts from Odoo Backend - Customer Wallet support",
    "summary": """
        Add customer wallet balance.""",
    "version": "12.0.1.0.0",
    "category": "Point of Sale",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SCRLfs",
    "maintainers": ["carmenbianca"],
    "license": "AGPL-3",
    "application": False,
    "auto_install": True,
    "depends": [
        "pos_print_receipt_backend",
        "pos_customer_wallet",
    ],
    "excludes": [],
    "data": [
        "report/report_pos_receipt.xml",
    ],
    "demo": [],
    "qweb": [],
}

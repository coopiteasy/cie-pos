# SPDX-FileCopyrightText: 2022 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Point of Sale Invoice Paid From Point of Sale",
    "summary": """
        Mark invoices that were paid from the POS as such, and remove the
        reference line from the invoice report document for these invoices.""",
    "version": "12.0.1.0.0",
    "category": "Point of Sale",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SC",
    "maintainers": ["carmenbianca"],
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "account",
        "point_of_sale",
    ],
    "excludes": [],
    "data": [
        "views/report_invoice.xml",
    ],
    "demo": [],
    "qweb": [],
}

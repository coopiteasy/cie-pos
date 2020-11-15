# Copyright 2020 - Today Coop IT Easy SCRLfs
#     Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Generate POS receipts from Odoo Backend",
    "version": "12.0.1.0.0",
    "author": "Coop IT Easy SCRLfs",
    "website": "https://coopiteasy.be",
    "license": "AGPL-3",
    "category": "Point of Sale",
    "summary": """
        This module helps you to print POS receipts from the Odoo backend
    """,
    "depends": ["point_of_sale"],
    "data": [
        "data/report_paperformat.xml",
        "report/report_pos_receipt.xml",
        "views/point_of_sale_report.xml",
        "views/pos_order_view.xml",
    ],
    "installable": True,
}

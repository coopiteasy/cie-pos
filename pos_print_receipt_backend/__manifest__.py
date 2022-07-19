# Copyright 2020 - Today Coop IT Easy SC
#     Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Generate POS receipts from Odoo Backend",
    "version": "12.0.1.1.1",
    "author": "Coop IT Easy SC",
    "website": "https://coopiteasy.be",
    "license": "AGPL-3",
    "category": "Point of Sale",
    "summary": """
        This module helps you to print and/or email POS receipts from the Odoo backend
    """,
    "depends": ["point_of_sale"],
    "data": [
        "data/report_paperformat.xml",
        "report/report_pos_receipt.xml",
        "views/point_of_sale_report.xml",
        "data/mail_template_data.xml",
        "wizard/pos_order_receipt_send_views.xml",
        "views/pos_order_view.xml",
    ],
    "installable": True,
}

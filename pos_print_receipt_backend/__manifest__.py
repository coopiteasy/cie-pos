# Copyright 2020 - Today Coop IT Easy SC
#     Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Generate POS receipts from Odoo Backend",
    "version": "16.0.1.0.0",
    "author": "Coop IT Easy SC",
    "website": "https://github.com/coopiteasy/cie-pos",
    "license": "AGPL-3",
    "category": "Point of Sale",
    "summary": """
        This module helps you to print and/or email POS receipts from the Odoo backend
    """,
    "depends": ["point_of_sale"],
    "data": [
        "data/report_paperformat.xml",  # used in point_of_sale_report
        "views/point_of_sale_report.xml",  # used in report_pos_receipt mail_template_data
        "data/mail_template_data.xml",
        "report/order_lines_receipt.xml",
        "report/report_pos_receipt.xml",
        "report/wrapped_product_name_lines.xml",
        "security/ir.model.access.csv",
        "views/pos_order_view.xml",
        "wizard/pos_order_receipt_send_views.xml",
    ],
    "assets": {
        "web.report_assets_common": [
            "/point_of_sale/static/src/css/pos_receipts.css",
            "/pos_print_receipt_backend/static/src/css/pos_receipt.css",
        ],
    },
}

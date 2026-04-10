# SPDX-FileCopyrightText: 2017 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "POS Products Display Customization",
    "summary": "Add display weight and supplier information on PoS product cards",
    "version": "16.0.1.0.0",
    "category": "Sales/Point of Sale",
    "website": "https://github.com/coopiteasy/cie-pos",
    "author": "Coop IT Easy SC",
    "license": "AGPL-3",
    "depends": [
        "beesdoo_product_label",
        "point_of_sale",
        "product_main_supplier",
    ],
    "assets": {
        "point_of_sale.assets": [
            "pos_products/static/src/js/**/*.js",
            "pos_products/static/src/xml/**/*.xml",
            "pos_products/static/src/scss/pos.scss",
        ],
    },
}

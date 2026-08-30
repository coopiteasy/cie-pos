# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "PoS Set Pricelist Restrict",
    "summary": "Restrict pricelist changes to managers in the Point of Sale",
    "version": "16.0.1.0.0",
    "category": "Point of Sale",
    "website": "https://github.com/coopiteasy/cie-pos",
    "author": "Coop IT Easy SC",
    "maintainers": ["mihien"],
    "license": "AGPL-3",
    "depends": [
        "point_of_sale",
    ],
    "data": [
        "views/res_config_settings_views.xml",
    ],
    "assets": {
        "point_of_sale.assets": [
            "pos_set_pricelist_restrict/static/src/js/**/*.esm.js",
            "pos_set_pricelist_restrict/static/src/xml/**/*.xml",
            "pos_set_pricelist_restrict/static/src/scss/pos.scss",
        ]
    },
}

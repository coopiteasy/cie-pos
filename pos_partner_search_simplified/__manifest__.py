# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "PoS Partner Search Simplified",
    "summary": "Limit partner search in the PoS to name and member code",
    "version": "16.0.1.0.0",
    "category": "Point Of Sale",
    "website": "https://github.com/coopiteasy/cie-pos",
    "author": "Coop IT Easy SC",
    "maintainers": ["mihien"],
    "license": "AGPL-3",
    "depends": [
        "point_of_sale",
    ],
    "assets": {
        "point_of_sale.assets": [
            "pos_partner_search_simplified/static/src/js/db.esm.js",
            "pos_partner_search_simplified/static/src/js/**/PartnerListScreen.esm.js",
        ]
    },
}

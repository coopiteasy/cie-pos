/** @odoo-module **/
// SPDX-FileCopyrightText: 2026 Coop IT Easy SC
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import PosDB from "point_of_sale.DB";

PosDB.include({
    _filter_partner_search_string(partner) {
        return {
            id: partner.id,
            name: partner.name,
            barcode: partner.barcode,
        };
    },
    _partner_search_string(partner) {
        return this._super(this._filter_partner_search_string(partner));
    },
});

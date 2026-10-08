/** @odoo-module **/
// SPDX-FileCopyrightText: 2026 Coop IT Easy SC
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import PartnerListScreen from "point_of_sale.PartnerListScreen";
import Registries from "point_of_sale.Registries";

export const PosPartnerSearchSimplifiedPartnerListScreen = (
    OriginalPartnerListScreen
) =>
    class extends OriginalPartnerListScreen {
        // Exact copy of getNewPartners, only with less search_fields
        // @override
        async getNewPartners() {
            const limit = 30;
            const domain = this._getPartnerSearchDomain(this.state.query);
            const result = await this.env.services.rpc(
                {
                    model: "pos.session",
                    method: "get_pos_ui_res_partner_by_params",
                    args: [
                        [odoo.pos_session_id],
                        {
                            domain,
                            limit: limit,
                            offset: this.state.currentOffset,
                        },
                    ],
                    context: this.env.session.user_context,
                },
                {
                    timeout: 3000,
                    shadow: true,
                }
            );
            return result;
        }

        _getPartnerSearchFields() {
            return ["name", "barcode"];
        }

        _getPartnerSearchDomain(query) {
            if (query) {
                const search_fields = this._getPartnerSearchFields();
                return [
                    ...Array(search_fields.length - 1).fill("|"),
                    ...search_fields.map((field) => [
                        field,
                        "ilike",
                        this.state.query + "%",
                    ]),
                ];
            }
            return [];
        }
    };

Registries.Component.extend(
    PartnerListScreen,
    PosPartnerSearchSimplifiedPartnerListScreen
);

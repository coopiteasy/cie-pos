/** @odoo-module **/
// SPDX-FileCopyrightText: 2026 Coop IT Easy SC
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import {Component} from "point_of_sale.Registries";
import PartnerDetailsEdit from "point_of_sale.PartnerDetailsEdit";

const RestrictPricelistPartnerDetailsEdit = (OriginalPartnerDetailsEdit) =>
    class extends OriginalPartnerDetailsEdit {
        get hasPricelistControlRights() {
            return (
                !this.env.pos.config.restrict_pricelist_control ||
                this.env.pos.get_cashier().role === "manager"
            );
        }
    };

Component.extend(PartnerDetailsEdit, RestrictPricelistPartnerDetailsEdit);

export default PartnerDetailsEdit;

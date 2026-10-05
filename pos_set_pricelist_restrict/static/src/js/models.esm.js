/** @odoo-module **/
// SPDX-FileCopyrightText: 2026 Coop IT Easy SC
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import {PosGlobalState} from "point_of_sale.models";
import Registries from "point_of_sale.Registries";

const RestrictPricelistPosGlobalState = (OriginalPosGlobalState) =>
    class extends OriginalPosGlobalState {
        get hasPricelistControlRights() {
            return (
                !this.config.restrict_pricelist_control ||
                this.get_cashier().role === "manager"
            );
        }
    };

Registries.Model.extend(PosGlobalState, RestrictPricelistPosGlobalState);

export default PosGlobalState;

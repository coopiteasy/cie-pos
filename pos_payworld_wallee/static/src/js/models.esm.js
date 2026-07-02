/** @odoo-module alias=pos_payworld_wallee.models **/
// SPDX-FileCopyrightText: 2026 Vincent Haulotte
// SPDX-FileCopyrightText: 2026 Coop IT Easy SC
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import {Payment, register_payment_method} from "point_of_sale.models";
import PaymentPayworldWallee from "pos_payworld_wallee.payment";
import Registries from "point_of_sale.Registries";

register_payment_method("payworld_wallee", PaymentPayworldWallee);

const PosPayworldWalleePayment = (Payment_) =>
    class extends Payment_ {
        constructor() {
            super(...arguments);
            this.terminalServiceId = this.terminalServiceId || null;
        }
        export_as_JSON() {
            const json = super.export_as_JSON(...arguments);
            json.terminal_service_id = this.terminalServiceId;
            return json;
        }
        init_from_JSON(json) {
            super.init_from_JSON(...arguments);
            this.terminalServiceId = json.terminal_service_id;
        }
        setTerminalServiceId(id) {
            this.terminalServiceId = id;
        }
    };

Registries.Model.extend(Payment, PosPayworldWalleePayment);

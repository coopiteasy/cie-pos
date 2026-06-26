odoo.define('pos_payworld_wallee.models', function (require) {
    'use strict';

    const { register_payment_method, Payment } = require('point_of_sale.models');
    const PaymentPayworldWallee = require('pos_payworld_wallee.payment');
    const Registries = require('point_of_sale.Registries');

    register_payment_method('payworld_wallee', PaymentPayworldWallee);

    const PosPayworldWalleePayment = (Payment) => class PosPayworldWalleePayment extends Payment {
        constructor(obj, options) {
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
});

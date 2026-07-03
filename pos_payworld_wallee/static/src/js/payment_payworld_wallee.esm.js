/** @odoo-module alias=pos_payworld_wallee.payment **/
// SPDX-FileCopyrightText: 2026 Vincent Haulotte
// SPDX-FileCopyrightText: 2026 Coop IT Easy SC
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import {Gui} from "point_of_sale.Gui";
import PaymentInterface from "point_of_sale.PaymentInterface";
import rpc from "web.rpc";

const CANCEL_TIMEOUT = 10000;
// Wallee terminal perform-transaction waits up to 90s for cardholder interaction.
const SEND_PAYMENT_REQUEST_TIMEOUT = 110000;
const NUM_SERVICE_ID_DIGITS = 10;
const CARD_TYPE = "Payworld/Wallee";

const PaymentPayworldWallee = PaymentInterface.extend({
    send_payment_request: function (cid) {
        this._super.apply(this, arguments);
        return this._wallee_pay(cid);
    },

    send_payment_cancel: function () {
        this._super.apply(this, arguments);
        return rpc
            .query(
                {
                    model: "pos.payment.method",
                    method: "wallee_cancel_payment_request",
                    args: [[this.payment_method.id], {}],
                },
                {timeout: CANCEL_TIMEOUT, shadow: true}
            )
            .then(() => {
                this._show_error(
                    this.pos.env._t(
                        "If the payment is already displayed on the terminal, cancel it manually on the terminal."
                    )
                );
                return false;
            });
    },

    _wallee_pay: function (cid) {
        const order = this.pos.get_order();
        const line = order.paymentlines.find((paymentLine) => paymentLine.cid === cid);

        if (!line) {
            return Promise.resolve(false);
        }
        if (line.amount <= 0) {
            this._show_error(
                this.pos.env._t("Cannot process a zero or negative amount.")
            );
            line.set_payment_status("retry");
            return Promise.resolve(false);
        }

        const serviceId = Math.floor(Math.random() * Math.pow(2, 64))
            .toString()
            .substring(0, NUM_SERVICE_ID_DIGITS);
        line.setTerminalServiceId(serviceId);
        line.set_payment_status("waitingCard");

        const data = {
            amount: line.amount,
            currency: this.pos.currency.name,
            reference: order.name || order.uid,
            order_uid: order.uid,
            pos_config_id: this.pos.config.id,
            service_id: serviceId,
        };

        return rpc
            .query(
                {
                    model: "pos.payment.method",
                    method: "wallee_send_payment_request",
                    args: [[this.payment_method.id], data],
                },
                {
                    timeout: SEND_PAYMENT_REQUEST_TIMEOUT,
                    shadow: true,
                }
            )
            .then((response) => {
                if (response && response.success) {
                    line.transaction_id = response.transaction_id || "";
                    line.card_type = CARD_TYPE;
                    line.set_payment_status("done");
                    return true;
                }
                const message =
                    (response && (response.message || response.state)) ||
                    this.pos.env._t("Payment was not successful.");
                this._show_error(
                    _.str.sprintf(
                        this.pos.env._t("Message from Payworld/Wallee: %s"),
                        message
                    )
                );
                line.set_payment_status("retry");
                return false;
            })
            .catch((error) => {
                console.error("Payworld/Wallee payment error", error);
                this._show_error(
                    this.pos.env._t(
                        "Could not connect to Odoo or Payworld/Wallee. Please check the connection and try again."
                    )
                );
                line.set_payment_status("retry");
                return false;
            });
    },

    _show_error: function (msg, title) {
        Gui.showPopup("ErrorPopup", {
            title: title || this.pos.env._t("Payworld/Wallee Error"),
            body: msg,
        });
    },
});

export default PaymentPayworldWallee;

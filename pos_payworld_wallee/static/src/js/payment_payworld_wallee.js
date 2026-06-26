odoo.define('pos_payworld_wallee.payment', function (require) {
    'use strict';

    const core = require('web.core');
    const rpc = require('web.rpc');
    const PaymentInterface = require('point_of_sale.PaymentInterface');
    const { Gui } = require('point_of_sale.Gui');

    const _t = core._t;

    const PaymentPayworldWallee = PaymentInterface.extend({
        send_payment_request: function (cid) {
            this._super.apply(this, arguments);
            return this._wallee_pay(cid);
        },

        send_payment_cancel: function () {
            this._super.apply(this, arguments);
            return rpc.query({
                model: 'pos.payment.method',
                method: 'wallee_cancel_payment_request',
                args: [[this.payment_method.id], {}],
            }, { timeout: 10000, shadow: true }).then(() => {
                this._show_error(_t('If the payment is already displayed on the terminal, cancel it manually on the terminal.'));
                return false;
            });
        },

        _wallee_pay: function (cid) {
            const order = this.pos.get_order();
            const line = order.paymentlines.find(paymentLine => paymentLine.cid === cid);

            if (!line) {
                return Promise.resolve(false);
            }
            if (line.amount <= 0) {
                this._show_error(_t('Cannot process a zero or negative amount.'));
                line.set_payment_status('retry');
                return Promise.resolve(false);
            }

            const serviceId = Math.floor(Math.random() * Math.pow(2, 64)).toString().substring(0, 10);
            line.setTerminalServiceId(serviceId);
            line.set_payment_status('waitingCard');

            const data = {
                amount: line.amount,
                currency: this.pos.currency.name,
                reference: order.name || order.uid,
                order_uid: order.uid,
                pos_config_id: this.pos.config.id,
                service_id: serviceId,
            };

            return rpc.query({
                model: 'pos.payment.method',
                method: 'wallee_send_payment_request',
                args: [[this.payment_method.id], data],
            }, {
                // Wallee terminal perform-transaction waits up to 90s for cardholder interaction.
                timeout: 110000,
                shadow: true,
            }).then((response) => {
                if (response && response.success) {
                    line.transaction_id = response.transaction_id || '';
                    line.card_type = 'Payworld/Wallee';
                    line.set_payment_status('done');
                    return true;
                }
                const message = response && (response.message || response.state) || _t('Payment was not successful.');
                this._show_error(_.str.sprintf(_t('Message from Payworld/Wallee: %s'), message));
                line.set_payment_status('retry');
                return false;
            }).catch((error) => {
                console.error('Payworld/Wallee payment error', error);
                this._show_error(_t('Could not connect to Odoo or Payworld/Wallee. Please check the connection and try again.'));
                line.set_payment_status('retry');
                return false;
            });
        },

        _show_error: function (msg, title) {
            Gui.showPopup('ErrorPopup', {
                title: title || _t('Payworld/Wallee Error'),
                body: msg,
            });
        },
    });

    return PaymentPayworldWallee;
});

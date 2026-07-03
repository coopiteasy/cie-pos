# SPDX-FileCopyrightText: 2026 Vincent Haulotte
# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import logging

from odoo import _, api, fields, models
from odoo.exceptions import AccessDenied, UserError, ValidationError

from ..lib.wallee_minimal import DEFAULT_API_URL, WalleeApiError, WalleeMinimalClient

_logger = logging.getLogger(__name__)

DEFAULT_CURRENCY = "EUR"
DEFAULT_REFERENCE = "Odoo POS"
MAX_REFERENCE_LENGTH = 100
MAX_LINE_ID_LENGTH = 200
MAX_RESPONSE_LENGTH = 5000


class PosPaymentMethod(models.Model):
    _inherit = "pos.payment.method"

    def _get_payment_terminal_selection(self):
        return super()._get_payment_terminal_selection() + [
            ("payworld_wallee", "Payworld / Wallee")
        ]

    wallee_space_id = fields.Integer(
        string="Wallee Space ID",
        copy=False,
        groups="base.group_erp_manager",
        help="Space ID provided by Payworld/Wallee.",
    )
    wallee_application_user_id = fields.Integer(
        string="Wallee Application User ID",
        copy=False,
        groups="base.group_erp_manager",
        help="Application user ID used to sign Wallee API requests.",
    )
    wallee_authentication_key = fields.Char(
        copy=False,
        groups="base.group_erp_manager",
        help="Authentication key for the Wallee application user.",
    )
    wallee_terminal_identifier = fields.Char(
        copy=False,
        help="Unique terminal identifier used by the Wallee Cloud Till Interface.",
    )
    wallee_api_url = fields.Char(
        string="Wallee API URL",
        default=DEFAULT_API_URL,
        groups="base.group_erp_manager",
        help="Keep default unless Payworld provides another URL.",
    )
    wallee_language = fields.Char(
        string="Terminal Language",
        default="fr-BE",
        help="Optional language sent to Wallee for the terminal transaction, "
        "e.g. fr-BE or en-US.",
    )
    wallee_latest_transaction_id = fields.Char(
        copy=False, groups="base.group_erp_manager"
    )
    wallee_latest_response = fields.Text(copy=False, groups="base.group_erp_manager")

    @api.constrains("wallee_terminal_identifier")
    def _check_wallee_terminal_identifier(self):
        for payment_method in self:
            if not payment_method.wallee_terminal_identifier:
                continue
            existing = self.sudo().search(
                [
                    ("id", "!=", payment_method.id),
                    (
                        "wallee_terminal_identifier",
                        "=",
                        payment_method.wallee_terminal_identifier,
                    ),
                ],
                limit=1,
            )
            if existing:
                raise ValidationError(
                    _(
                        "Terminal %(wallee_terminal_identifier)s is already "
                        "used on payment method %(payment_method_name)s.",
                        wallee_terminal_identifier=(
                            payment_method.wallee_terminal_identifier
                        ),
                        payment_method_name=existing.display_name,
                    )
                )

    def _is_write_forbidden(self, fields):
        whitelisted_fields = {"wallee_latest_transaction_id", "wallee_latest_response"}
        return super()._is_write_forbidden(fields - whitelisted_fields)

    def _check_pos_user(self):
        if not self.env.su and not self.user_has_groups("point_of_sale.group_pos_user"):
            raise AccessDenied()

    def _wallee_client(self):
        self.ensure_one()
        sudo_self = self.sudo()
        if (
            not sudo_self.wallee_application_user_id
            or not sudo_self.wallee_authentication_key
        ):
            raise UserError(
                _("Missing Wallee application user ID or authentication key.")
            )
        return WalleeMinimalClient(
            user_id=sudo_self.wallee_application_user_id,
            authentication_key=sudo_self.wallee_authentication_key,
            api_url=sudo_self.wallee_api_url,
        )

    def _wallee_amount(self, amount, currency):
        # the amount sent by the pos is sometimes not exactly rounded, like
        # 8.29 being transmitted as 8.290000000000001, and in this case wallee
        # returns a 422 error saying "The number 8.290000000000001 needs to
        # have at most 11 integer digits and at most 8 decimal digits.".
        # odoo.tools.float_round() rounds in the same way as the pos thus
        # leaving this value unchanged. python built-in round() handles this
        # correctly, probably because it uses a higher precision.
        return round(amount, currency.decimal_places)

    def _extract_transaction_state(self, transaction):
        value = transaction.get("state") if isinstance(transaction, dict) else None
        if isinstance(value, dict):
            value = value.get("id") or value.get("name") or value.get("state")
        return str(value or "").upper()

    def _extract_transaction_id(self, transaction):
        if isinstance(transaction, dict):
            return transaction.get("id")
        return None

    def _is_success_state(self, state):
        return state in {
            "FULFILL",
            "FULFILLING",
            "COMPLETED",
            "SUCCESSFUL",
            "AUTHORIZED",
            "CONFIRMED",
        }

    def _is_failed_state(self, state):
        return state in {
            "FAILED",
            "VOIDED",
            "DECLINE",
            "DECLINED",
            "CANCELED",
            "CANCELLED",
        }

    def wallee_send_payment_request(self, data):
        """Create a Wallee transaction and send it to the configured terminal."""
        self.ensure_one()
        sudo_self = self.sudo()
        self._check_pos_user()
        if not data:
            raise UserError(_("Invalid Wallee request."))
        if self.use_payment_terminal != "payworld_wallee":
            raise UserError(
                _("This payment method is not configured for Payworld/Wallee.")
            )

        currency = self.env["res.currency"].browse(data.get("currency_id"))
        if not currency:
            raise UserError(_("Missing or invalid currency_id."))

        amount = self._wallee_amount(data.get("amount"), currency)
        if amount <= 0:
            raise UserError(_("Cannot process a zero or negative amount."))

        space_id = int(sudo_self.wallee_space_id or 0)
        terminal_identifier = sudo_self.wallee_terminal_identifier
        if not space_id or not terminal_identifier:
            raise UserError(_("Missing Wallee Space ID or terminal identifier."))

        reference = (
            data.get("reference") or data.get("order_uid") or DEFAULT_REFERENCE
        )[:MAX_REFERENCE_LENGTH]
        language = sudo_self.wallee_language or None
        client = self._wallee_client()

        transaction_create = {
            "currency": currency.name,
            "merchantReference": reference,
            "lineItems": [
                {
                    "name": _("Odoo POS payment"),
                    "uniqueId": (data.get("order_uid") or reference or "pos")[
                        :MAX_LINE_ID_LENGTH
                    ],
                    "quantity": 1,
                    "amountIncludingTax": amount,
                    "type": "PRODUCT",
                }
            ],
            "metaData": {
                "odoo_pos_order_uid": str(data.get("order_uid") or ""),
                "odoo_pos_config_id": str(data.get("pos_config_id") or ""),
                "odoo_payment_method_id": str(self.id),
            },
            "autoConfirmationEnabled": True,
            "chargeRetryEnabled": False,
            "emailsDisabled": True,
        }

        try:
            transaction = client.create_transaction(
                space_id=space_id,
                transaction_create=transaction_create,
                expand=["state"],
            )
            transaction_id = self._extract_transaction_id(transaction)
            if not transaction_id:
                raise UserError(_("Wallee did not return a transaction ID."))

            sudo_self.write({"wallee_latest_transaction_id": str(transaction_id)})
            result = client.perform_transaction_by_identifier(
                space_id=space_id,
                identifier=terminal_identifier,
                transaction_id=int(transaction_id),
                language=language,
                expand=["state", "paymentConnectorConfiguration", "terminal"],
            )
            state = self._extract_transaction_state(result)
            sudo_self.write(
                {"wallee_latest_response": str(result)[:MAX_RESPONSE_LENGTH]}
            )

            return {
                "success": self._is_success_state(state),
                "failed": self._is_failed_state(state),
                "state": state,
                "transaction_id": str(
                    self._extract_transaction_id(result) or transaction_id
                ),
                "raw": result,
            }
        except WalleeApiError as exc:
            _logger.exception("Payworld/Wallee API payment failed")
            return {
                "success": False,
                "failed": True,
                "state": "ERROR",
                "message": str(exc),
            }
        except Exception as exc:
            _logger.exception("Payworld/Wallee terminal payment failed")
            return {
                "success": False,
                "failed": True,
                "state": "ERROR",
                "message": str(exc),
            }

    def wallee_cancel_payment_request(self, data=None):
        self.ensure_one()
        self._check_pos_user()
        return {
            "success": False,
            "message": _("Cancel manually on the terminal if needed."),
        }

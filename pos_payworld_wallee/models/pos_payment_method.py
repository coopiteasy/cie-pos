# -*- coding: utf-8 -*-
import logging
from decimal import Decimal, ROUND_HALF_UP

from odoo import api, fields, models, _
from odoo.exceptions import AccessDenied, UserError, ValidationError

from ..lib.wallee_minimal import WalleeMinimalClient, WalleeApiError

_logger = logging.getLogger(__name__)


class PosPaymentMethod(models.Model):
    _inherit = 'pos.payment.method'

    def _get_payment_terminal_selection(self):
        return super()._get_payment_terminal_selection() + [('payworld_wallee', 'Payworld / Wallee')]

    wallee_space_id = fields.Integer(
        string='Wallee Space ID',
        copy=False,
        groups='base.group_erp_manager',
        help='Space ID provided by Payworld/Wallee.',
    )
    wallee_application_user_id = fields.Integer(
        string='Wallee Application User ID',
        copy=False,
        groups='base.group_erp_manager',
        help='Application user ID used to sign Wallee API requests.',
    )
    wallee_authentication_key = fields.Char(
        string='Wallee Authentication Key',
        copy=False,
        groups='base.group_erp_manager',
        help='Authentication key for the Wallee application user.',
    )
    wallee_terminal_identifier = fields.Char(
        string='Wallee Terminal Identifier',
        copy=False,
        help='Unique terminal identifier used by the Wallee Cloud Till Interface.',
    )
    wallee_api_host = fields.Char(
        string='Wallee API Host',
        default='https://app-wallee.com/api/v2.0',
        groups='base.group_erp_manager',
        help='Keep default unless Payworld provides another host.',
    )
    wallee_language = fields.Char(
        string='Terminal Language',
        default='fr-BE',
        help='Optional language sent to Wallee for the terminal transaction, e.g. fr-BE or en-US.',
    )
    wallee_latest_transaction_id = fields.Char(copy=False, groups='base.group_erp_manager')
    wallee_latest_response = fields.Text(copy=False, groups='base.group_erp_manager')

    @api.constrains('wallee_terminal_identifier')
    def _check_wallee_terminal_identifier(self):
        for payment_method in self:
            if not payment_method.wallee_terminal_identifier:
                continue
            existing = self.sudo().search([
                ('id', '!=', payment_method.id),
                ('wallee_terminal_identifier', '=', payment_method.wallee_terminal_identifier),
            ], limit=1)
            if existing:
                raise ValidationError(_('Terminal %s is already used on payment method %s.') % (
                    payment_method.wallee_terminal_identifier,
                    existing.display_name,
                ))

    def _is_write_forbidden(self, fields):
        whitelisted_fields = {'wallee_latest_transaction_id', 'wallee_latest_response'}
        return super()._is_write_forbidden(fields - whitelisted_fields)

    def _check_pos_user(self):
        if not self.env.su and not self.user_has_groups('point_of_sale.group_pos_user'):
            raise AccessDenied()

    def _wallee_client(self):
        self.ensure_one()
        if not self.sudo().wallee_application_user_id or not self.sudo().wallee_authentication_key:
            raise UserError(_('Missing Wallee application user ID or authentication key.'))
        return WalleeMinimalClient(
            user_id=int(self.sudo().wallee_application_user_id),
            authentication_key=self.sudo().wallee_authentication_key,
            host=self.sudo().wallee_api_host or 'https://app-wallee.com/api/v2.0',
            timeout=25,
        )

    def _wallee_amount(self, amount):
        return float(Decimal(str(amount)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

    def _extract_transaction_state(self, transaction):
        value = transaction.get('state') if isinstance(transaction, dict) else None
        if isinstance(value, dict):
            value = value.get('id') or value.get('name') or value.get('state')
        return str(value or '').upper()

    def _extract_transaction_id(self, transaction):
        if isinstance(transaction, dict):
            return transaction.get('id')
        return None

    def _is_success_state(self, state):
        return state in {'FULFILL', 'FULFILLING', 'COMPLETED', 'SUCCESSFUL', 'AUTHORIZED', 'CONFIRMED'}

    def _is_failed_state(self, state):
        return state in {'FAILED', 'VOIDED', 'DECLINE', 'DECLINED', 'CANCELED', 'CANCELLED'}

    def wallee_send_payment_request(self, data):
        """Create a Wallee transaction and send it to the configured terminal."""
        self.ensure_one()
        self._check_pos_user()
        if not data:
            raise UserError(_('Invalid Wallee request.'))
        if self.use_payment_terminal != 'payworld_wallee':
            raise UserError(_('This payment method is not configured for Payworld/Wallee.'))

        amount = self._wallee_amount(data.get('amount'))
        if amount <= 0:
            raise UserError(_('Cannot process a zero or negative amount.'))

        space_id = int(self.sudo().wallee_space_id or 0)
        terminal_identifier = self.sudo().wallee_terminal_identifier
        if not space_id or not terminal_identifier:
            raise UserError(_('Missing Wallee Space ID or terminal identifier.'))

        currency = data.get('currency') or 'EUR'
        reference = (data.get('reference') or data.get('order_uid') or 'Odoo POS')[:100]
        language = self.sudo().wallee_language or None
        client = self._wallee_client()

        transaction_create = {
            'currency': currency,
            'merchantReference': reference,
            'lineItems': [{
                'name': _('Odoo POS payment'),
                'uniqueId': (data.get('order_uid') or reference or 'pos')[:200],
                'quantity': 1,
                'amountIncludingTax': amount,
                'type': 'PRODUCT',
            }],
            'metaData': {
                'odoo_pos_order_uid': str(data.get('order_uid') or ''),
                'odoo_pos_config_id': str(data.get('pos_config_id') or ''),
                'odoo_payment_method_id': str(self.id),
            },
            'autoConfirmationEnabled': True,
            'chargeRetryEnabled': False,
            'emailsDisabled': True,
        }

        try:
            transaction = client.create_transaction(
                space_id=space_id,
                transaction_create=transaction_create,
                expand=['state'],
            )
            transaction_id = self._extract_transaction_id(transaction)
            if not transaction_id:
                raise UserError(_('Wallee did not return a transaction ID.'))

            self.sudo().write({'wallee_latest_transaction_id': str(transaction_id)})
            result = client.perform_transaction_by_identifier(
                space_id=space_id,
                identifier=terminal_identifier,
                transaction_id=int(transaction_id),
                language=language,
                expand=['state', 'paymentConnectorConfiguration', 'terminal'],
            )
            state = self._extract_transaction_state(result)
            self.sudo().write({'wallee_latest_response': str(result)[:5000]})

            return {
                'success': self._is_success_state(state),
                'failed': self._is_failed_state(state),
                'state': state,
                'transaction_id': str(self._extract_transaction_id(result) or transaction_id),
                'raw': result,
            }
        except WalleeApiError as exc:
            _logger.exception('Payworld/Wallee API payment failed')
            return {
                'success': False,
                'failed': True,
                'state': 'ERROR',
                'message': str(exc),
            }
        except Exception as exc:
            _logger.exception('Payworld/Wallee terminal payment failed')
            return {
                'success': False,
                'failed': True,
                'state': 'ERROR',
                'message': str(exc),
            }

    def wallee_cancel_payment_request(self, data=None):
        self.ensure_one()
        self._check_pos_user()
        return {'success': False, 'message': _('Cancel manually on the terminal if needed.')}

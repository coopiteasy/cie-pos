# POS Payworld / Wallee Terminal for Odoo 16

Initial Odoo 16 module for integrating Payworld/Wallee payment terminals with the POS.
This module targets the **Cloud Till Interface** pattern with the official Wallee Python SDK https://github.com/wallee-payment/python-sdk.
It is intentionally limited to the first WooCoop need:

- send the POS amount and reference to the terminal;
- wait for success/failure from the terminal;
- mark the Odoo POS payment line as done or retry.

Not included in this first version: refunds, reversals, tips, final balance, offline mode.

## Deployment approach

This avoids a server-level `pip install wallee`.

Instead of bundling the full generated SDK, the module includes a very small embedded client in:

```text
pos_payworld_wallee/lib/wallee_minimal.py
```

It implements only the two API calls required for the first WooCoop use case:

- `POST /payment/transactions` to create a transaction;
- `POST /payment/terminals/by-identifier/{identifier}/perform-transaction` to trigger the terminal payment.

The authentication logic follows the official Wallee SDK pattern: an HS256 JWT is generated and sent as `Authorization: Bearer ...`, signed with the base64-decoded application user's authentication key.

## Why not bundle the full SDK?

The official Wallee Python SDK is Apache-2.0 and could technically be vendored, but it brings extra dependencies such as `urllib3`, `pydantic` and `PyJWT`, plus a large generated codebase. For this Odoo module with a very narrow POS terminal scope, the embedded minimal client is easier to review and deploy.

## Odoo configuration

In **Point of Sale > Configuration > Payment Methods**:

1. Select **Use a Payment Terminal = Payworld / Wallee**.
2. Fill in:
   - Wallee Space ID
   - Wallee API Host, normally `https://app-wallee.com/api/v2.0`
   - Wallee Application User ID
   - Wallee Authentication Key
   - Wallee Terminal Identifier
   - Terminal Language, e.g. `fr-BE`

Then add that payment method to the relevant POS configuration.

## Initial scope

- One payment terminal per POS payment method.
- Cloud Till Interface / long-polling HTTP flow.
- Send amount and POS reference to terminal.
- Wait for terminal result and mark POS payment line done/retry.
- No refunds, reversals, tips or final balance in this version.

## Validation needed with Payworld

Before production use, confirm with Payworld:

- exact terminal identifier expected;
- final success state returned after Bancontact/card payments;
- whether a specific payment method configuration/brand must be restricted;
- cancellation/reversal API to use if cashier cancels from Odoo.

POS Payworld / Wallee Terminal integration for Odoo 16.

Initial scope:

- One payment terminal per POS payment method.
- Cloud Till Interface via Wallee Python SDK.
- Send amount and POS reference to terminal.
- Wait for terminal result and mark POS payment line done/retry.
- No refunds, reversals, tips or final balance in this first version.

No server-level Python dependency: minimal Wallee REST client embedded in module.

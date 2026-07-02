Initial Odoo 16 module for integrating Payworld/Wallee payment terminals with the POS.
This module targets the **Cloud Till Interface** pattern with the official Wallee Python SDK https://github.com/wallee-payment/python-sdk.
It is intentionally limited to the first WooCoop need:

- send the POS amount and reference to the terminal;
- wait for success/failure from the terminal;
- mark the Odoo POS payment line as done or retry.

Not included in this first version: refunds, reversals, tips, final balance, offline mode.

Validation needed with Payworld
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before production use, confirm with Payworld:

- exact terminal identifier expected;
- final success state returned after Bancontact/card payments;
- whether a specific payment method configuration/brand must be restricted;
- cancellation/reversal API to use if cashier cancels from Odoo.

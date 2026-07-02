Deployment approach
~~~~~~~~~~~~~~~~~~~

This avoids a server-level ``pip install wallee``.

Instead of bundling the full generated SDK, the module includes a very small embedded client in:

::

    pos_payworld_wallee/lib/wallee_minimal.py

It implements only the two API calls required for the first WooCoop use case:

- ``POST /payment/transactions`` to create a transaction;
- ``POST /payment/terminals/by-identifier/{identifier}/perform-transaction`` to trigger the terminal payment.

The authentication logic follows the official Wallee SDK pattern: an HS256 JWT is generated and sent as ``Authorization: Bearer ...``, signed with the base64-decoded application user's authentication key.

Why not bundle the full SDK?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The official Wallee Python SDK is Apache-2.0 and could technically be vendored, but it brings extra dependencies such as ``urllib3``, ``pydantic`` and ``PyJWT``, plus a large generated codebase. For this Odoo module with a very narrow POS terminal scope, the embedded minimal client is easier to review and deploy.

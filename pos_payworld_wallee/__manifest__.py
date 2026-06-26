# -*- coding: utf-8 -*-
{
    'name': 'POS Payworld / Wallee Terminal',
    'version': '16.0.1.1.0',
    'category': 'Sales/Point of Sale',
    'summary': 'Integrate Odoo POS with Payworld/Wallee cloud payment terminals',
    'description': '''
POS Payworld / Wallee Terminal integration for Odoo 16.

Initial scope:
- One payment terminal per POS payment method.
- Cloud Till Interface via Wallee Python SDK.
- Send amount and POS reference to terminal.
- Wait for terminal result and mark POS payment line done/retry.
- No refunds, reversals, tips or final balance in this first version.

No server-level Python dependency: minimal Wallee REST client embedded in module.
''',
    'depends': ['point_of_sale'],
    'data': [
        'views/pos_payment_method_views.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'pos_payworld_wallee/static/src/js/**/*',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}

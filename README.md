
<!-- /!\ Non OCA Context : Set here the badge of your runbot / runboat instance. -->
[![Pre-commit Status](https://github.com/coopiteasy/cie-pos/actions/workflows/pre-commit.yml/badge.svg?branch=12.0)](https://github.com/coopiteasy/cie-pos/actions/workflows/pre-commit.yml?query=branch%3A12.0)
[![Build Status](https://github.com/coopiteasy/cie-pos/actions/workflows/test.yml/badge.svg?branch=12.0)](https://github.com/coopiteasy/cie-pos/actions/workflows/test.yml?query=branch%3A12.0)
[![codecov](https://codecov.io/gh/coopiteasy/cie-pos/branch/12.0/graph/badge.svg)](https://codecov.io/gh/coopiteasy/cie-pos)
<!-- /!\ Non OCA Context : Set here the badge of your translation instance. -->

<!-- /!\ do not modify above this line -->

# Coop IT Easy Point of Sale modules

TODO: add repo description.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->
[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[pos_account_invoice_access_right](pos_account_invoice_access_right/) | 12.0.1.0.1 |  | Allows read access on `account.invoice` to `point_of_sale.group_pos_user`
[pos_category_display](pos_category_display/) | 12.0.1.0.1 |  | TODO
[pos_customer_selection](pos_customer_selection/) | 12.0.1.0.1 |  | Allows a faster customer research and selection
[pos_default_quantity](pos_default_quantity/) | 12.0.1.0.1 |  | When adding an to order line, this module sets the quantity to the default quantity set on the product unit category.
[pos_order_taxes_fix](pos_order_taxes_fix/) | 12.0.1.0.1 |  | Adds a button to on pos session to fix the taxes of the orders that doesn't match the calculation on backend"
[pos_print_receipt_backend](pos_print_receipt_backend/) | 12.0.1.1.1 |  | This module helps you to print and/or email POS receipts from the Odoo backend
[pos_products](pos_products/) | 12.0.1.0.1 |  | Adds information on POS product card. - display weight - producers
[pos_remove_0_qty](pos_remove_0_qty/) | 12.0.1.0.1 |  | Remove pos order line with quantity set to 0
[pos_round_cash_payment](pos_round_cash_payment/) | 12.0.1.0.1 |  | Rounds due amount to nearest 5 cents when adding a cash Payment line.
[pos_search_accented_unaccented](pos_search_accented_unaccented/) | 12.0.1.0.1 |  | Allows to search in POS for products with accented characters in name using unaccented search query.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Coop IT Easy SC
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
<!-- /!\ Non OCA Context : Set here the full description of your organization. -->

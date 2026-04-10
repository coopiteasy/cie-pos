/** @odoo-module **/
// SPDX-FileCopyrightText: 2026 Coop IT Easy SC
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import {Component} from "point_of_sale.Registries";
import ProductItem from "point_of_sale.ProductItem";

const PosProductsProductItem = (OriginalProductItem) =>
    class extends OriginalProductItem {
        get formatted_display_weight() {
            return (
                String(this.props.product.display_weight).replace(
                    ".",
                    this.env._t.database.parameters.decimal_point
                ) +
                " " +
                this.props.product.display_unit[1]
            );
        }
    };

Component.extend(ProductItem, PosProductsProductItem);

export default ProductItem;

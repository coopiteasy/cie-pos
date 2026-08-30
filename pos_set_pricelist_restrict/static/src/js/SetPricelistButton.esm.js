/** @odoo-module **/
// SPDX-FileCopyrightText: 2026 Coop IT Easy SC
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import {Component} from "point_of_sale.Registries";
import SetPricelistButton from "point_of_sale.SetPricelistButton";

const RestrictPricelistSetPricelistButton = (OriginalSetPricelistButton) =>
    class extends OriginalSetPricelistButton {
        get hasPricelistControlRights() {
            return (
                !this.env.pos.config.restrict_pricelist_control ||
                this.env.pos.get_cashier().role === "manager"
            );
        }
        async onClick() {
            if (!this.hasPricelistControlRights) {
                await this.showPopup("ErrorPopup", {
                    title: this.env._t("Access Denied"),
                    body: this.env._t("You must be a manager to change the pricelist."),
                });
                return;
            }
            return super.onClick();
        }
    };

Component.extend(SetPricelistButton, RestrictPricelistSetPricelistButton);

export default SetPricelistButton;

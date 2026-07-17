# Copyright 2021 Coop IT Easy SC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models
from odoo.tools import float_round, get_lang


class PosOrder(models.Model):
    _inherit = "pos.order"

    receipt_sent = fields.Boolean(
        string="Receipt sent by backend interface",
        readonly=True,
        default=False,
        copy=False,
        help="It indicates that the receipt has been sent.",
    )

    def receipt_print(self):
        self.filtered(lambda o: not o.receipt_sent).write({"receipt_sent": True})
        return (
            self.env.ref("pos_print_receipt_backend.action_report_receipt")
            .with_context(discard_logo_check=True)
            .report_action(self)
        )

    def action_send_and_print(self):
        return {
            "name": _("Send Receipt"),
            "res_model": "pos.order.receipt.send",
            "view_mode": "form",
            "context": {
                "default_email_layout_xmlid": "mail.mail_notification_layout",
                "default_template_id": self.env.ref(
                    "pos_print_receipt_backend.email_template_pos_order_receipt"
                ).id,
                "mark_receipt_as_sent": True,
                "active_model": "pos.order",
                # Setting both active_id and active_ids is required, mimicking how
                # direct call to ir.actions.act_window works
                "active_id": self.ids[0],
                "active_ids": self.ids,
            },
            "target": "new",
            "type": "ir.actions.act_window",
        }

    def action_receipt_sent(self):
        """Open a window to compose an email, with
        email_template_pos_order_receipt message loaded by default
        """
        self.ensure_one()
        template = self.env.ref(
            "pos_print_receipt_backend.email_template_pos_order_receipt",
            raise_if_not_found=False,
        )
        lang = False
        if template:
            lang = template._render_lang(self.ids)[self.id]
        if not lang:
            lang = get_lang(self.env).code
        compose_form = self.env.ref(
            "pos_print_receipt_backend.pos_order_send_wizard_form",
            raise_if_not_found=False,
        )
        ctx = dict(
            default_model="pos.order",
            default_res_id=self.id,
            # For the sake of consistency we need a default_res_model if
            # default_res_id is set. Not renaming default_model as it can
            # create many side-effects
            default_res_model="pos.order",
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode="comment",
            mark_receipt_as_sent=True,
            force_email=True,
            default_email_layout_xmlid="mail.mail_notification_layout",
            active_ids=self.ids,
        )
        report_action = {
            "name": _("Send Receipt"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "pos.order.receipt.send",
            "views": [(compose_form.id, "form")],
            "view_id": compose_form.id,
            "target": "new",
            "context": ctx,
        }

        if (
            self.env.is_admin()
            and not self.env.company.external_report_layout_id
            and not self.env.context.get("discard_logo_check")
        ):
            return self.env[
                "ir.actions.report"
            ]._action_configure_external_report_layout(report_action)

        return report_action

    def get_rounding_applied(self):
        """
        Return the cash rounding amount applied to this order

        :return: float, 0.0 if no rounding was applied
        """
        self.ensure_one()
        rounding_applied = float_round(
            self.amount_paid - self.amount_total,
            precision_rounding=self.currency_id.rounding,
        )
        return rounding_applied

    def get_total_discount(self):
        """
        Return the total discount amount across all lines, tax-inclusive.

        :return: float, 0.0 if no discounts were applied
        """
        self.ensure_one()
        return sum(
            line.get_price_with_tax_before_discount() * line.discount / 100
            for line in self.lines
        )

    def get_tax_details_grouped(self):
        """
        Return tax details grouped by tax, similar to ReportSaleDetails.get_sale_details()

        """
        self.ensure_one()
        taxes = {}

        for line in self.lines:
            line_taxes = line.tax_ids_after_fiscal_position.sudo().compute_all(
                line.price_unit * (1 - (line.discount or 0.0) / 100.0),
                self.pricelist_id.currency_id,
                line.qty,
                product=line.product_id,
                partner=line.order_id.partner_id or False,
            )
            for tax in line_taxes["taxes"]:
                taxes.setdefault(tax["id"], {"name": tax["name"], "tax_amount": 0.0})
                taxes[tax["id"]]["tax_amount"] += tax["amount"]

        return list(taxes.values())


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    MAX_RECEIPT_LINE_LENGTH = 24  # 40 * line ratio of .6, matches PoS JS

    def generate_product_name_wrapped(self):
        """
        Split this line's full product name into lines of at most
        MAX_RECEIPT_LINE_LENGTH characters, breaking only on spaces.

        This mirrors Odoo 16.0 PoS's JS implementation
        (models.js: generate_wrapped_product_name) so receipts printed
        from the backend match the ones printed from the PoS UI.

        :return: list of str, one per wrapped line
        """
        self.ensure_one()

        max_length = self.MAX_RECEIPT_LINE_LENGTH
        name = self.full_product_name or ""

        wrapped = []
        current_line = ""

        while len(name) > 0:
            space_index = name.find(" ")
            if space_index == -1:
                space_index = len(name)

            if len(current_line) + space_index > max_length:
                if len(current_line):
                    wrapped.append(current_line)
                current_line = ""

            current_line += name[0 : space_index + 1]
            name = name[space_index + 1 :]

        if len(current_line):
            wrapped.append(current_line)

        return wrapped

    def is_simple(self):
        """
        Return True if the line needs no extra detail on the receipt
        (no discount, unit-of-measure is units, quantity is 1, and the
        'without_discount' policy is not revealing a hidden markdown).

        Mirrors Odoo 16.0 PoS JS: isSimple (OrderReceipt.js)
        """
        self.ensure_one()
        return (
            self.discount == 0
            and self.product_uom_id == self.env.ref("uom.product_uom_unit")
            and self.qty == 1
            and not (
                self.order_id.pricelist_id.discount_policy == "without_discount"
                and self.price_unit < self.product_id.lst_price
            )
        )

    def has_visible_discount(self):
        """
        Return True if a discount should be shown on an order line of the receipt
        """
        self.ensure_one()
        if self.price_unit == self.product_id.lst_price:
            return False
        pricelist = self.order_id.pricelist_id
        return not pricelist or pricelist.discount_policy == "without_discount"

    def get_price_with_tax_before_discount(self):
        """
        Return the unit price including taxes, before discount.
        Mirrors the PoS JS price_with_tax_before_discount.
        """
        self.ensure_one()
        taxes = self.tax_ids_after_fiscal_position
        if not taxes:
            return self.price_unit
        tax_res = taxes.compute_all(
            self.price_unit,
            currency=self.order_id.pricelist_id.currency_id,
            quantity=self.qty,
            product=self.product_id,
            partner=self.order_id.partner_id,
        )
        return tax_res["total_included"]

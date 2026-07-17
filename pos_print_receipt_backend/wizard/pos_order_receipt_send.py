from odoo import _, api, fields, models
from odoo.tools.misc import get_lang

from odoo.addons.mail.wizard.mail_compose_message import _reopen


# Heavily based on AccountInvoiceSend with only two changes
# 1) Replacing invoices with orders
# 2) Contrary to account moves, pos orders don't need to store every related
#   communications and their attachments -> removed related logic handling
#   message_main_attachment_id and two fields from AccountInvoiceSend:
#   display_attachment_fields and attachments_not_supported
class PosReceiptSend(models.TransientModel):
    _name = "pos.order.receipt.send"
    _inherits = {"mail.compose.message": "composer_id"}
    _description = "POS Receipt Send"

    is_email = fields.Boolean("Email", default=True)
    receipt_without_email = fields.Text(
        compute="_compute_receipt_without_email",
        string="receipt(s) that will not be sent",
    )
    is_print = fields.Boolean("Print", default=False)
    order_ids = fields.Many2many(
        "pos.order", "pos_order_pos_order_receipt_send_rel", string="Orders"
    )
    composer_id = fields.Many2one(
        "mail.compose.message",
        string="Composer",
        required=True,
        ondelete="cascade",
    )
    template_id = fields.Many2one(
        "mail.template",
        "Use template",
        index=True,
        domain="[('model', '=', 'pos.order')]",
    )

    @api.model
    def default_get(self, fields):
        res = super(PosReceiptSend, self).default_get(fields)
        res_ids = self._context.get("active_ids")
        composer = self.env["mail.compose.message"].create(
            {"composition_mode": "comment" if len(res_ids) == 1 else "mass_mail"}
        )
        res.update({"order_ids": res_ids, "composer_id": composer.id})
        return res

    @api.onchange("order_ids")
    def _compute_composition_mode(self):
        for wizard in self:
            wizard.composition_mode = (
                "comment" if len(wizard.order_ids) == 1 else "mass_mail"
            )

    @api.onchange("template_id")
    def onchange_template_id(self):
        for wizard in self:
            if wizard.composer_id:
                wizard.composer_id.template_id = wizard.template_id.id
                wizard._compute_composition_mode()
                wizard.composer_id._onchange_template_id_wrapper()

    @api.onchange("is_email")
    def onchange_is_email(self):
        if self.is_email:
            res_ids = self._context.get("active_ids")
            if not self.composer_id:
                self.composer_id = self.env["mail.compose.message"].create(
                    {
                        "composition_mode": "comment"
                        if len(res_ids) == 1
                        else "mass_mail",
                        "template_id": self.template_id.id,
                    }
                )
            else:
                self.composer_id.composition_mode = (
                    "comment" if len(res_ids) == 1 else "mass_mail"
                )
                self.composer_id.template_id = self.template_id.id
                self._compute_composition_mode()
            self.composer_id._onchange_template_id_wrapper()

    @api.onchange("is_email")
    def _compute_receipt_without_email(self):
        for wizard in self:
            if wizard.is_email and len(wizard.order_ids) > 1:
                orders = self.env["pos.order"].search(
                    [
                        ("id", "in", self.env.context.get("active_ids")),
                        ("partner_id.email", "=", False),
                    ]
                )
                if orders:
                    wizard.receipt_without_email = "{}\n{}".format(
                        _(
                            "The following receipt(s) will not be sent by email, "
                            "because the customers don't have email address."
                        ),
                        "\n".join([o.pos_reference or o.name for o in orders]),
                    )
                else:
                    wizard.receipt_without_email = False
            else:
                wizard.receipt_without_email = False

    def _send_email(self):
        if self.is_email:
            # with_context : we don't want to reimport the file we just exported.
            self.composer_id.with_context(
                mail_notify_author=self.env.user.partner_id
                in self.composer_id.partner_ids,
                mailing_document_based=True,
            )._action_send_mail()
            if self.env.context.get("mark_receipt_as_sent"):
                # PoS user without writing rights should be able to change the flag
                self.mapped("order_ids").sudo().write({"receipt_sent": True})

    def _print_document(self):
        """to override for each type of models that will use this composer."""
        self.ensure_one()
        action = self.order_ids.receipt_print()
        action.update({"close_on_report_download": True})
        return action

    def send_and_print_action(self):
        self.ensure_one()
        # Send the mails in the correct language by splitting the ids per lang.
        # This should ideally be fixed in mail_compose_message,
        # so when a fix is made there this whole commit should be reverted.
        # basically self.body (which could be manually edited) extracts
        # self.template_id, which is then not translated for each customer.
        if self.composition_mode == "mass_mail" and self.template_id:
            active_ids = self.env.context.get("active_ids", self.res_id)
            active_records = self.env[self.model].browse(active_ids)
            langs = set(active_records.mapped("partner_id.lang"))
            for lang in langs:
                active_ids_lang = active_records.filtered(
                    lambda r: r.partner_id.lang == lang
                ).ids
                self_lang = self.with_context(
                    active_ids=active_ids_lang, lang=get_lang(self.env, lang).code
                )
                self_lang.onchange_template_id()
                self_lang._send_email()
        else:
            active_record = self.env[self.model].browse(self.res_id)
            lang = get_lang(self.env, active_record.partner_id.lang).code
            self.with_context(lang=lang)._send_email()
        if self.is_print:
            return self._print_document()
        return {"type": "ir.actions.act_window_close"}

    def save_as_template(self):
        self.ensure_one()
        self.composer_id.action_save_as_template()
        self.template_id = self.composer_id.template_id.id
        action = _reopen(self, self.id, self.model, context=self._context)
        action.update({"name": _("Send Receipt")})
        return action

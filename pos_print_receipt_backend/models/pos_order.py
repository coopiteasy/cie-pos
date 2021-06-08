from odoo import _, api, fields, models


class PosOrder(models.Model):
    _inherit = "pos.order"

    receipt_sent = fields.Boolean(
        string="Receipt sent by backend interface",
        readonly=True,
        default=False,
        copy=False,
        help="It indicates that the receipt has been sent.",
    )

    @api.multi
    def receipt_print(self):
        self.filtered(lambda o: not o.receipt_sent).write(
            {"receipt_sent": True}
        )
        return (
            self.env.ref("pos_print_receipt_backend.action_report_receipt")
            .with_context(discard_logo_check=True)
            .report_action(self)
        )

    @api.multi
    def action_receipt_sent(self):
        """ Open a window to compose an email, with
            email_template_pos_order_receipt message loaded by default
        """
        self.ensure_one()
        template = self.env.ref(
            "pos_print_receipt_backend.email_template_pos_order_receipt", False
        )
        compose_form = self.env.ref(
            "pos_print_receipt_backend.pos_order_send_wizard_form", False
        )
        # have model_description in template language
        lang = self.env.context.get("lang")
        if template and template.lang:
            lang = template._render_template(
                template.lang, "pos.order", self.id
            )
        self = self.with_context(lang=lang)
        ctx = dict(
            default_model="pos.order",
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode="comment",
            mark_receipt_as_sent=True,
            force_email=True,
        )
        return {
            "name": _("Send Receipt"),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "pos.order.receipt.send",
            "views": [(compose_form.id, "form")],
            "view_id": compose_form.id,
            "target": "new",
            "context": ctx,
        }

    @api.model
    def send_mail_receipt(self, pos_reference, email, body_from_ui, force=True):
        order = self.search([("pos_reference", "=", pos_reference)])

        order.note = "{}\n{} UTC Attempting to send mail receipt ".format(
            order.note or "", fields.datetime.now()
        )

        return super(PosOrder, self).send_mail_receipt(
            pos_reference, email, body_from_ui, force=True
        )

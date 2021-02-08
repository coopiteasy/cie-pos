# Copyright 2019 Coop IT Easy SCRLfs
# 	    Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class Container(models.Model):
    _name = "pos.container"
    _description = "Container for bulk items"

    name = fields.Char(string="Name")
    barcode = fields.Char("Barcode", size=13)
    weight = fields.Float(string="Weight (kg)")
    owner_id = fields.Many2one(
        comodel_name="res.partner",
        inverse_name="container_ids",
        string="Owner",
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        required=True,
        default=lambda self: self.env.user.company_id.currency_id,
    )
    deposit_value = fields.Monetary(
        string="Deposit Value", default=0.0, currency_field="currency_id"
    )
    state = fields.Selection(
        [("in", "Store"), ("out", "Customer")], default="in"
    )

    _sql_constraints = [
        (
            "barcode_uniq",
            "unique(barcode)",
            "A barcode can only be assigned to one container !",
        )
    ]

    @api.model
    def create_from_ui(self, container):
        container_id = container.pop("id", False)
        if container_id:  # Modifying existing container
            self.browse(container_id).write(container)
        else:
            container_id = self.create(container).id
        return container_id

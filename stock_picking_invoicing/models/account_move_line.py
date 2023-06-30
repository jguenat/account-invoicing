# Copyright (C) 2023-Today: Odoo Community Association
# @ 2023-Today: Akretion - www.akretion.com.br -
#   Magno Costa <magno.costa@akretion.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.depends("product_id", "product_uom_id")
    def _compute_price_unit(self):
        for line in self:
            if not line.move_line_ids:
                return super()._compute_price_unit()

            if not line.product_id or line.display_type in (
                "line_section",
                "line_note",
            ):
                continue
            if line.move_id.is_sale_document(include_receipts=True):
                document_type = "sale"
            elif line.move_id.is_purchase_document(include_receipts=True):
                document_type = "purchase"
            else:
                document_type = "other"

            product_price_unit = None
            if line.move_line_ids[0].invoice_state:
                product_price_unit = line.move_line_ids[0]._get_price_unit_invoice(
                    line.move_id.move_type, line.partner_id
                )

            line.price_unit = line.product_id._get_tax_included_unit_price(
                line.move_id.company_id,
                line.move_id.currency_id,
                line.move_id.date,
                document_type,
                fiscal_position=line.move_id.fiscal_position_id,
                product_uom=line.product_uom_id,
                product_price_unit=product_price_unit,
            )

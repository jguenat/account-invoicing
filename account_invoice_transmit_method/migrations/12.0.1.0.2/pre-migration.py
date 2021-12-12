# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    _field_renames = [
        ('res.partner', 'res_partner', 'customer_invoice_transmit_method_id', 'customer_invoice_transmit_method_id_temp'),
        ('res.partner', 'res_partner', 'supplier_invoice_transmit_method_id', 'supplier_invoice_transmit_method_id_temp'),
    ]
    openupgrade.rename_fields(env, _field_renames)

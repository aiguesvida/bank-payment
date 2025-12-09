# Copyright 2025 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

_logger = logging.getLogger(__name__)


def pre_init_hook(env):
    """
    Check if the payment method 'sepa_direct_debit' already exists.
    If it exists but lacks the XML ID, create the XML ID to prevent UniqueViolation
    during data loading.
    Using raw SQL for robustness.
    Odoo 19 passes 'env' to pre_init_hook.
    """
    cr = env.cr
    code = "sepa_direct_debit"
    payment_type = "inbound"
    module = "account_banking_sepa_direct_debit"
    xml_name = "sepa_direct_debit"

    # Check if existing mapping
    cr.execute(
        "SELECT res_id FROM ir_model_data WHERE module=%s AND name=%s",
        (module, xml_name),
    )
    if cr.fetchone():
        return

    # Check if payment method exists
    cr.execute(
        "SELECT id FROM account_payment_method WHERE code=%s AND payment_type=%s",
        (code, payment_type),
    )
    row = cr.fetchone()
    if row:
        res_id = row[0]
        _logger.info(
            "Found existing payment method '%s' (ID %s) without XML ID. Creating mapping.",
            code,
            res_id,
        )
        cr.execute(
            """
            INSERT INTO ir_model_data (module, name, model, res_id, noupdate)
            VALUES (%s, %s, 'account.payment.method', %s, true)
            ON CONFLICT DO NOTHING
            """,
            (module, xml_name, res_id),
        )

# Copyright 2025 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

_logger = logging.getLogger(__name__)


from odoo import api, SUPERUSER_ID

def pre_init_hook(cr):
    """
    Check if the payment method 'sepa_direct_debit' already exists.
    If it exists but lacks the XML ID, create the XML ID to prevent UniqueViolation
    during data loading.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    xml_id = "account_banking_sepa_direct_debit.sepa_direct_debit"
    code = "sepa_direct_debit"
    payment_type = "inbound"

    # Check if the XML ID already exists
    if env["ir.model.data"].search_count([("module", "=", "account_banking_sepa_direct_debit"), ("name", "=", "sepa_direct_debit")]):
        return

    # Check if the record exists by code/type
    payment_method = env["account.payment.method"].search([
        ("code", "=", code),
        ("payment_type", "=", payment_type),
    ], limit=1)

    if payment_method:
        _logger.info("Found existing payment method '%s' without XML ID. Creating XML ID '%s'.", code, xml_id)
        env["ir.model.data"].create({
            "module": "account_banking_sepa_direct_debit",
            "name": "sepa_direct_debit",
            "model": "account.payment.method",
            "res_id": payment_method.id,
            "noupdate": True,
        })

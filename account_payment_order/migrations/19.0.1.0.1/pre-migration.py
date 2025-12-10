# Copyright 2025 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """
    Delete all views for account.payment.order to force clean recreation.
    This fixes corrupted views that prevent proper form display.
    """
    _logger.info("Cleaning up all views for account.payment.order...")

    # Delete ir_model_data references for views
    cr.execute(
        """
        DELETE FROM ir_model_data 
        WHERE model = 'ir.ui.view' 
        AND res_id IN (
            SELECT id FROM ir_ui_view 
            WHERE model = 'account.payment.order'
        )
        """
    )

    # Delete all views for this model
    cr.execute(
        """
        DELETE FROM ir_ui_view 
        WHERE model = 'account.payment.order'
        """
    )

    _logger.info("All account.payment.order views deleted. They will be recreated on module load.")

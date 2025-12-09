# Copyright 2025 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """
    Delete potentially corrupted search view record to allow clean recreation.
    """
    _logger.info("Cleaning up potentially corrupted search view for account.banking.mandate...")
    
    # Delete the ir_model_data reference
    cr.execute(
        """
        DELETE FROM ir_model_data 
        WHERE module = 'account_banking_mandate' 
        AND name = 'view_mandate_search'
        """
    )
    
    # Delete any view with this name for this model
    cr.execute(
        """
        DELETE FROM ir_ui_view 
        WHERE model = 'account.banking.mandate' 
        AND name = 'account.banking.mandate.search'
        """
    )
    
    _logger.info("Search view cleanup completed.")

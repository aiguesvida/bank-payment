# Copyright 2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class AccountPaymentMethod(models.Model):
    _inherit = "account.payment.method"

    pain_version = fields.Selection([], string="PAIN Version")
    convert_to_ascii = fields.Boolean(
        string="Convert to ASCII",
        default=True,
        help="If active, Odoo will convert each accented character to "
        "the corresponding unaccented character, so that only ASCII "
        "characters are used in the generated PAIN file.",
    )
    warn_not_sepa = fields.Boolean(string="Warn If Not SEPA")

    def get_xsd_file_path(self):
        """This method is designed to be inherited in the SEPA modules"""
        self.ensure_one()
        raise UserError(_("No XSD file path found for payment method '%s'") % self.name)

    @api.constrains("code", "payment_type", "pain_version")
    def _check_code_payment_type_unique(self):
        for rec in self:
            if not rec.code:
                continue
            domain = [
                ("code", "=", rec.code),
                ("payment_type", "=", rec.payment_type),
                ("pain_version", "=", rec.pain_version),
                ("id", "!=", rec.id),
            ]
            if self.search_count(domain):
                raise ValidationError(
                    _(
                        "A payment method of the same type already exists with this code and PAIN version"
                    )
                )

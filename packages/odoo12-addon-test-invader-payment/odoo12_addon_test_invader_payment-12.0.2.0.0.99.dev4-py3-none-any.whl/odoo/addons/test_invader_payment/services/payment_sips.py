# Copyright 2019 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


class PaymentServiceSips(Component):
    _name = "test.payment.service.sips"
    _inherit = "payment.service.sips"
    _collection = "res.partner"

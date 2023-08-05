# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.component.core import Component
from http import HTTPStatus

from odoo.http import Response


# from odoo.addons.sm_rest_api.models.models import validate_request


class PartnerService(Component):
  _inherit = 'base.rest.service'
  _name = 'partago_partner.service'
  _usage = 'partago-partner'
  _collection = 'partago_partner.rest.public.services'
  _description = """
    Partner Services
    Access to the partner services is only allowed to authenticated users.
    If you are not authenticated go to <a href='/web/login'>Login</a>
  """

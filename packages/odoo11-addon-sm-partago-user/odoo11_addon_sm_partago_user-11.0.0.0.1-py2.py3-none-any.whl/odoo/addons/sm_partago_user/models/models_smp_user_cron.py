from odoo import models, fields, api
from odoo.addons.sommobilitat.models.models_sommobilitat_utils import sommobilitat_utils
from odoo.addons.sm_partago_user.models.models_carsharing_update_data_fetch_wizard import carsharing_update_data_fetch_wizard
from odoo.addons.sm_partago_db.models.models_smp_db_utils import smp_db_utils
from odoo.addons.sm_maintenance.models.models_sm_utils import sm_utils
from odoo.addons.sm_partago_user.models.models_smp_user_utils import smp_user_utils
from datetime import datetime


class smp_user_cron(models.Model):
  _name = 'sm_partago_user.smp_user_cron'

  #
  # CS UPDATE DATA
  #
  
  @api.model
  def fetch_and_complete_cs_update_data_from_wp(self):
    _sm_utils = sommobilitat_utils.get_instance()
    _sm_utils.fetch_wp_users(self)
    #TODO: move fetching and complete mechanism to smp_utils
    carsharing_update_data_fetch_wizard.fetch_carsharing_update_data(self.env)
    self._complete_missing_data_requests()

  def _complete_missing_data_requests(self):
    not_completed_updates = self.env['sm_partago_user.carsharing_update_data'].search(
      [('final_state', '=', 'not_completed')])
    if not_completed_updates.exists():
      for update_data in not_completed_updates:
        update_data.complete_request()

  #
  # CS COMPLETE REGISTRATIONS
  #
  def complete_cs_registrations(self):
    _smp_user_utils = smp_user_utils.get_instance()
    _smp_user_utils.register_in_carsharing_cron(self)

  #
  # MEMBER CS GROUPS
  #
  @api.model
  def auto_update_member_cs_groups(self):
    app_db_utils = smp_db_utils.get_instance()
    app_db_utils.update_all_system_db_data_from_app_db(self)
    self._fetch_carsharing_groups()

  def _fetch_carsharing_groups(self):
    cs_members = self.env['res.partner'].search([('cs_person_index', '!=', '')])
    if cs_members.exists():
      for cs_member in cs_members:
        cs_member.get_carsharing_groups()

  #
  # MEMBER CS STATUS
  #
  def update_members_carsharing_registration_status(self):
    app_user_utils = smp_user_utils.get_instance()
    app_user_utils.update_members_carsharing_registration_status_cron(self)
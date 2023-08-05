# -*- coding: utf-8 -*-
from html.parser import HTMLParser
from datetime import datetime

from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.addons.sm_maintenance.models.models_sm_utils import sm_utils

class carsharing_update_data(models.Model):
  _name = 'sm_partago_user.carsharing_update_data'

  related_member_id = fields.Many2one('res.partner', string=_("Related member"))
  parent_id = fields.Many2one('res.partner', string=_("Related company"))
  form_id = fields.Char(string=_("wp entry ID"))
  cs_update_type = fields.Char(string=_("Registration type"))
  cs_update_name = fields.Char(string=_("Firstname"))
  cs_update_first_surname = fields.Char(string=_("First surname"))
  cs_update_second_surname = fields.Char(string=_("Second surname"))
  cs_update_dni = fields.Char(string=_("DNI/NIF"))
  cs_update_dni_image = fields.Char(string=_("DNI/NIF Image"))
  cs_update_email = fields.Char(string=_("Email"))
  cs_update_mobile = fields.Char(string=_("Phone"))
  cs_update_birthday = fields.Date(string=_("Birthdate"))
  cs_update_driving_license_expiration_date = fields.Date(string=_("Driving license. Expiricy date"))
  cs_update_image_driving_license = fields.Char(string=_("Driving license. Image"))
  cs_update_comments = fields.Char(string=_("Comments"))
  cs_update_cif = fields.Char(string=_("CIF"))
  cs_update_group = fields.Char(string=_("Group"))
  cs_update_group_secondary = fields.Char(string=_("Group (secondary"))
  cs_fetch_date = fields.Date(string=_("Fetch Date"))
  cs_complete_date = fields.Date(string=_("Completed Date"))

  #TODO: Maybe we remove this. Not so nice with 2 states.
  state = fields.Selection([
    ('new', 'New'),
    # ('complete', 'Completed'),
    ('completed','Completed')
  ], default='new')

  final_state = fields.Selection([
    ('not_completed', 'Not completed'),
    ('cs_company_member', 'CS company member created & registration request'),
    ('soci_not_found', 'Soci not found'),
    ('data_updated', 'Data updated & registration request'),
  ], default='not_completed')

  cs_registration_request_ids = fields.One2many(comodel_name='sm_partago_user.carsharing_registration_request',
    inverse_name='related_cs_update_data_id', string=_("Registration request:"))

  _order = "id desc"


  @api.multi
  def complete_action(self):
    if self.final_state == 'not_completed':
      self.complete_request()

  def complete_request(self):
    final_state = 'not_completed'
    mail_template = False
    # COMPANY REGISTRATION
    if self.cs_update_type == "company":
      success = self._create_company_user()
      if success:
        final_state = 'cs_company_member'
        self._create_registration_request()
      else:
        #TODO: Company user error must send only one email, not one every hour!!
        error_msg = _("""CS UPDATE DATA Company error. Company not found on system. CS_update_data: %s""") % (str(self.id))
        sm_utils.create_system_task(self,"CS company user error.",error_msg)
    # MEMBER UPDATE / CS REGISTRATION
    else:
      success = self._compute_related_member()
      if success:
        final_state = 'data_updated'
        self._update_cs_data()
        create_request = True
        if not self.cs_update_group and not self.cs_update_group_secondary and self.related_member_id.cs_state == 'active':
          create_request = False
          sm_utils.send_email_from_template(self.related_member_id, 'cs_already_active')
        if create_request:
          self._create_registration_request()
        # TODO: should we send this email. When there is a registration request we shouldn't
        # mail_template = 'cs_complete_data_successful_email_template_id'
      else:
        final_state = 'soci_not_found'
        mail_template = 'cs_complete_data_soci_not_found_email_template_id'
    self._set_completed(final_state, mail_template)

  def _set_completed(self, final_state=False, mail_template=False):
    if final_state != 'not_completed':
      u_data = {
        'state': 'completed',
        'cs_complete_date': datetime.today(),
        'final_state': final_state
      }
      if mail_template:
        if mail_template == 'cs_complete_data_soci_not_found_email_template_id':
          sm_utils.send_email_from_template(self, mail_template)
        else:
          sm_utils.send_email_from_template(self.related_member_id, mail_template)
      self.write(u_data)

  def _create_registration_request(self):
    self.env['sm_partago_user.carsharing_registration_request'].create({
      'related_member_id': self.related_member_id.id,
      'force_registration': False,
      'group_index': self.cs_update_group,
      'ba_behaviour': 'no_ba',
      'related_cs_update_data_id': self.id
    })
    if self.cs_update_group_secondary:
      if self.cs_update_group_secondary != '':
        self.env['sm_partago_user.carsharing_registration_request'].create({
          'related_member_id': self.related_member_id.id,
          'force_registration': False,
          'group_index': self.cs_update_group_secondary,
          'ba_behaviour': 'no_ba',
          'related_cs_update_data_id': self.id
        })

  def _compute_related_member(self):
    h = HTMLParser()
    update_dni = str(self.cs_update_dni).replace("-", "").replace(" ", "").upper()
    query = [('dni', '=', update_dni),('cs_user_type', '!=', 'organisation')]
    related_members = self.env['res.partner'].search(query, order="id asc")
    if related_members.exists():
      # return first related member having same email
      for rmember in related_members:
        if rmember.email == self.cs_update_email:
          self.write({'related_member_id': rmember.id})
          return True
      # return first related member for query
      self.write({'related_member_id': related_members[0].id})
      return True
    return False

  #
  # CS USERS: UPDATE
  #
  def _update_cs_data(self):
    if self.related_member_id:
      self.related_member_id.write(self._get_update_data())

  def _get_update_data(self):
    cs_member_dict = {}
    if self.cs_update_name:
      cs_member_dict["firstname"] = self.cs_update_name
    if self.cs_update_first_surname:
      cs_member_dict["first_surname"] = self.cs_update_first_surname
    if self.cs_update_second_surname:
      cs_member_dict["second_surname"] = self.cs_update_second_surname
    # TODO: review this. Member must handle this automathically
    if self.cs_update_first_surname and self.cs_update_second_surname:
      cs_member_dict["surname"] = self.cs_update_first_surname + " " + self.cs_update_second_surname
    if self.cs_update_name and self.cs_update_first_surname and self.cs_update_second_surname:
      cs_member_dict[
        "name"] = self.cs_update_first_surname + " " + self.cs_update_second_surname + ", " + self.cs_update_name
    if self.cs_update_dni:
      cs_member_dict["dni"] = self.cs_update_dni
    if self.cs_update_email:
      cs_member_dict["email"] = self.cs_update_email
    if self.cs_update_mobile:
      cs_member_dict["phone"] = self.cs_update_mobile
    if self.cs_update_birthday:
      cs_member_dict["birthday"] = self.cs_update_birthday
    if self.parent_id and self.cs_update_type == "company":
      cs_member_dict["parent_id"] = self.parent_id.id
    if self.cs_update_driving_license_expiration_date:
      cs_member_dict["driving_license_expiration_date"] = self.cs_update_driving_license_expiration_date
    if self.cs_update_image_driving_license:
      cs_member_dict["image_driving_license"] = self.cs_update_image_driving_license
    if self.cs_update_dni_image:
      cs_member_dict["image_dni"] = self.cs_update_dni_image

    return cs_member_dict

  # 
  # COMPANY USERS
  # 
  def _compute_related_company(self):
    h = HTMLParser()
    related_company = self.env['res.partner'].search([
      ('cif', '=', str(self.cs_update_cif).replace(" ", "").upper()),
      ('is_company','=',True)
    ], order="id desc")
    if related_company.exists():
      self.write({'parent_id': related_company[0].id})
      return True
    return False

  def _create_company_user(self):
    success = self._compute_related_company()
    if success:
      self._create_member({
        'cs_user_type': 'organisation',
        'is_company': False,
        'company_type': 'person',
        'lang' : 'ca_ES'
      })
      return True
    return False

  def _create_member(self, extra_data={}):
    u_data = self._get_update_data()
    u_data.update(extra_data)
    new_member = self.env['res.partner'].create(u_data)
    self.write({'related_member_id': new_member.id})
    return True

  # @api.model
  # def update_cs_update_data_action(self):
  #   if self.env.context:
  #     if 'active_ids' in self.env.context:
  #       cs_updates = self.env['sm_partago_user.carsharing_update_data'].browse(
  #         self.env.context['active_ids'])
  #       if cs_updates.exists():
  #         for cs_update in cs_updates:
  #           u_data = {}
  #           if cs_update.state:
  #             if cs_update.state == 'complete':
  #               u_data['state'] = 'completed'
  #           if cs_update.final_state:
  #             # if cs_update.final_state == 'not_completed' or \
  #             if cs_update.final_state == 'soci_not_found' or \
  #               cs_update.final_state == 'cs_company_member':
  #               u_data['final_state'] = cs_update.final_state
  #             else:
  #               u_data['final_state'] = 'data_updated'
  #           if bool(u_data):
  #             cs_update.write(u_data)
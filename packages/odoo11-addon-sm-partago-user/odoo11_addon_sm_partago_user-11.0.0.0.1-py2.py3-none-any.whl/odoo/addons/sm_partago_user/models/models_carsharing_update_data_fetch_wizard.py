from datetime import datetime
from html.parser import HTMLParser

from odoo import models, api
from odoo.addons.sm_connect.models.models_sm_wordpress_db_utils import sm_wordpress_db_utils


class carsharing_update_data_fetch_wizard(models.TransientModel):
  _name = "sm_partago_user.carsharing_update_data_fetch_wizard"

  @api.multi
  def create_request(self):
    carsharing_update_data_fetch_wizard.fetch_carsharing_update_data(self.env)
    return True

  @staticmethod
  def carsharing_fields_map():
    return {
      'complete_member_type': 'cs_update_type',
      'complete_member_nom': 'cs_update_name',
      'complete_member_first_surname': 'cs_update_first_surname',
      'complete_member_second_surname': 'cs_update_second_surname',
      'complete_member_dninif': 'cs_update_dni',
      'complete_member_image_dninif': 'cs_update_dni_image',
      'complete_member_email': 'cs_update_email',
      'complete_member_first_tel': 'cs_update_mobile',
      'complete_member_birthday_date': 'cs_update_birthday',
      'complete_member_driving_license_expiration_date': 'cs_update_driving_license_expiration_date',
      'complete_member_image_driving_license': 'cs_update_image_driving_license',
      'complete_member_comment': 'cs_update_comments',
      'complete_member_cif_empresa': 'cs_update_cif',
      # 'complete_member_group_config': 'cs_update_group_config',
      'complete_member_group': 'cs_update_group',
      'complete_member_secondary_group': 'cs_update_group_secondary'
    }

  @staticmethod
  def fetch_carsharing_update_data(env):
    member_context = env['res.partner']
    __db_utils = sm_wordpress_db_utils.get_instance()
    args = {
      'post_type': 'sm_carsharing',
      'orderby': 'ID',
      'order': 'DESC',
      'number': 9999
    }
    fmap = carsharing_update_data_fetch_wizard.carsharing_fields_map()
    carsharing_posts = __db_utils.get_posts(args)
    h = HTMLParser()
    for carsharing_post in carsharing_posts:
      # carsharing és el número de post
      mcm = carsharing_post.custom_fields
      m_data = {
        'form_id': str(carsharing_post)
      }
      for cf in mcm:
        if cf['key'] in fmap:
          if cf['key'] == 'complete_member_birthday_date':
            bd = False
            try:
              bd = datetime.strptime(cf['value'], "%d/%m/%Y")
            except ValueError:
              print("member" + str(carsharing_dninif) + " has no correct datebirth")
            if bd:
              m_data[fmap[cf['key']]] = bd.strftime("%Y-%m-%d")
          elif cf['key'] == 'complete_member_driving_license_expiration_date':
            bd = False
            try:
              bd = datetime.strptime(cf['value'], "%d/%m/%Y")
            except ValueError:
              print("member" + str(carsharing_dninif) + " has no correct driving license expiration date")
            if bd:
              m_data[fmap[cf['key']]] = bd.strftime("%Y-%m-%d")
          elif cf['key'] == 'complete_member_type':
            if cf['value'] == 'persona':
              m_data[fmap[cf['key']]] = 'person'
            else:
              m_data[fmap[cf['key']]] = 'company'
          elif cf['key'] == 'complete_member_dninif':
            m_data[fmap[cf['key']]] = str(cf['value']).replace("-", "").replace(" ", "").upper()
          # elif cf['key'] == 'complete_member_comment':
          #   # TODO: send an email to carsharing
          else:
            m_data[fmap[cf['key']]] = h.unescape(cf['value'])

      if not carsharing_update_data_fetch_wizard.already_updated(env, m_data['form_id']):
        m_data["cs_fetch_date"] = datetime.today().strftime("%Y-%m-%d")
        env['sm_partago_user.carsharing_update_data'].create(m_data)
      else:
        break
    return True

  @staticmethod
  def already_updated(env, update_id):
    if env['sm_partago_user.carsharing_update_data'].search([('form_id', '=', update_id)]):
      return True
    return False
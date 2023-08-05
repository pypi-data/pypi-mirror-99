from html.parser import HTMLParser
from datetime import datetime
from odoo.addons.sm_connect.models.models_sm_wordpress_db_utils import sm_wordpress_db_utils
from odoo.addons.sm_maintenance.models.models_sm_utils import sm_utils
# TODO: change this from fetch to API strategy
class sommobilitat_utils(object):

  __instance = None

  @staticmethod
  def get_instance():
    if sommobilitat_utils.__instance is None:
      sommobilitat_utils()
    return sommobilitat_utils.__instance

  def __init__(self):
    if sommobilitat_utils.__instance is not None:
      raise Exception("This class is a singleton!")
    else:
      sommobilitat_utils.__instance = self

  def fetch_wp_users(self, parent):
    h = HTMLParser()
    db_utils = sm_wordpress_db_utils.get_instance()
    last_wp_member_id = self.get_system_last_member_wp_id(parent)
    args = {
      'post_type': 'sm_member',
      'orderby': 'ID',
      'order': 'DESC',
      'number': 100
    }
    wp_members = db_utils.get_posts(args)
    if wp_members:
      for wp_member in wp_members:
        if int(wp_member.id) > int(last_wp_member_id):
          data = self.parse_wp_member_data_for_system_member(parent, wp_member)
          if data:
            m_data = data['m_data']
            system_member = parent.env['res.partner'].search([('wp_member_id','=',m_data['wp_member_id'])])
            if not system_member.exists():
              system_member_c = parent.env['res.partner'].create(m_data)
              system_member = system_member_c[0]
              # if creation coupon create related coupon and wait for rewards to do the rest
              if system_member.creation_coupon:
                query = [('name', '=', system_member.creation_coupon), ('related_member_id', '=', system_member.id)]
                creation_data = {
                  'name': system_member.creation_coupon,
                  'related_member_id': system_member.id,
                  'wp_member_id': system_member.wp_member_id
                }
                related_member_coupon = sm_utils.get_create_existing_model(
                  parent.env['sm_rewards.sm_member_related_coupon'], query, creation_data)
              # no creation coupon but still want to register? can create registration request
              else:
                if data['cs_registration'] and system_member.company_type!='company':
                  rr_data = self.parse_wp_member_data_for_system_registration_request(wp_member,system_member)
                  if rr_data:
                    parent.env['sm_partago_user.carsharing_registration_request'].create(rr_data)

              system_member.activate_member()
              if system_member.company_type == 'company':
                system_member.set_registration_coupon()
        else:
          break
    return True

  def parse_wp_member_data_for_system_registration_request(self, wp_member, system_member):
    if wp_member:
      fmap = self.fields_map()
      m_data = {}
      h = HTMLParser()
      cs_registration = False
      for custom_field in wp_member.custom_fields:
        if custom_field['key'] == 'member_details_reward_group':
          m_data['group_index'] = custom_field['value']

        config = False
        if custom_field['key'] == 'member_details_reward_group_config':
          config = custom_field['value']
        
        m_data['force_registration'] = False
        if custom_field['key'] == 'member_details_force_cs_registration':
          if custom_field['value'] == 1:
            m_data['force_registration'] = True
        
        m_data['ba_behaviour'] = 'no_ba'
        if custom_field['key'] == 'member_details_cs_dedicated_ba':
          if custom_field['value'] == 1:
            m_data['ba_behaviour'] = 'dedicated_ba'

        # TODO: Remove this hardcoded shit
        if config == "gl_vic" and system_member.cs_user_type == 'organisation' and 'group_index' not in m_data.keys():
          m_data['group_index'] = 'gt_uviccampus'
          m_data['force_registration'] = True
      
      if bool(m_data):
        m_data['related_member_id'] = system_member.id
        return m_data
      return False

  def fields_map(self):
    return {
      'member_details_type': 'company_type',
      'member_details_name': 'firstname',
      # 'member_details_surname': 'surname',  # backwards compatibility
      'member_details_surname_1': 'first_surname',
      'member_details_surname_2': 'second_surname',
      'member_details_socialr': 'social_reason',
      'member_details_dni': 'dni',
      'member_details_cif': 'cif',
      'member_details_representative': 'representative',
      'member_details_email': 'email',
      'member_details_phone1': 'phone',
      'member_details_phone2': 'phone_2',
      'member_details_datebirth': 'birthday',
      'member_details_address': 'street',
      'member_details_zip': 'zip',
      'member_details_province': 'state',
      'member_details_town': 'city',
      'member_details_atype': 'bank_account_type',
      'member_details_iban1': 'iban_1',
      'member_details_iban2': 'iban_2',
      'member_details_iban3': 'iban_3',
      'member_details_iban4': 'iban_4',
      'member_details_iban5': 'iban_5',
      'member_details_iban6': 'iban_6',
      'member_details_member_nr': 'member_nr',
      'member_details_related_company': 'parent_id',
      'member_details_inscripcio_complerta': 'membership_success',
      'image_dni': 'image_dni',
      'image_driving_license': 'image_driving_license',
      'driving_license_expiration_date': 'driving_license_expiration_date',
      'member_details_coupon': 'creation_coupon',
      'member_details_register_carsharing': 'cs_force_registration',
      # Not needed. Will disapear from system_member
      # 'member_details_bulleti': 'newsletter_subscription',
      # 'member_details_reward_group_config': 'member_group_config',
      # 'member_details_reward_group': 'member_group',
      # 'member_details_force_cs_registration': 'cs_force_registration_without_data'
    }

  def get_system_last_member_wp_id(self,parent):
    system_members = parent.env['res.partner'].search([], order="id desc")
    if (system_members.exists()):
      for member in system_members:
        if member.wp_member_id:
          return int(member.wp_member_id)
    return 0

  def parse_wp_member_data_for_system_member(self,parent, wp_member):
    if wp_member:
      fmap = self.fields_map()
      m_data = {
        'wp_member_id': wp_member.id
      }
      h = HTMLParser()
      cs_registration = False
      for cf in wp_member.custom_fields:
        if cf['key'] in fmap:
          if cf['key'] == 'member_details_datebirth':
            bd = False
            try:
              bd = datetime.strptime(cf['value'], "%d/%m/%Y")
            except ValueError:
              print("member" + str(wp_member) + " has no correct datebirth")
            if bd:
              m_data[fmap[cf['key']]] = bd.strftime("%Y-%m-%d")

          elif cf['key'] == 'member_details_type':
            if cf['value'] == 'persona':
              m_data[fmap[cf['key']]] = 'person'
              m_data['is_company'] = False
            else:
              m_data[fmap[cf['key']]] = 'company'
              m_data['is_company'] = True

          elif cf['key'] == 'member_details_related_company':
            if bool(cf['value']):
              group_config = cf['value']
              related_company = parent.env['res.partner'].search([
                ('cif', '=', group_config)
              ], order="member_nr desc")
              if related_company.exists():
                m_data['parent_id'] = related_company[0].id

          elif cf['key'] == 'member_details_inscripcio_complerta':
            if cf['value']:
              m_data[fmap[cf['key']]] = False
              if cf['value'] == '1':
                m_data[fmap[cf['key']]] = True

          elif cf['key'] == 'member_details_email':
            if cf['value']:
              m_data[fmap[cf['key']]] = str(cf['value']).lower().strip()
              m_data['invoicing_email'] = m_data[fmap[cf['key']]]

          elif cf['key'] == 'member_details_coupon':
            if cf['value']:
              m_data[fmap[cf['key']]] = str(cf['value']).upper().strip()

          elif cf['key'] == 'member_details_dni':
            if cf['value']:
              m_data['dni'] = str(cf['value']).replace("-", "").replace(" ", "").upper()

          elif cf['key'] == 'member_details_cif':
            if cf['value']:
              m_data['cif'] = str(cf['value']).replace("-", "").replace(" ", "").upper()

          elif cf['key'] == 'member_details_register_carsharing':
            if cf['value']:
              if cf['value'] == '1':
                cs_registration = True

          elif cf['key'] == 'member_details_member_nr':
            if int(cf['value']) > 0:
              m_data[fmap[cf['key']]] = int(cf['value'])
            else:
              if str(cf['value']) == '-1':
                m_data[fmap[cf['key']]] = 'promo'
              if str(cf['value']) == '-3':
                m_data[fmap[cf['key']]] = 'organisation'

          else:
            m_data[fmap[cf['key']]] = h.unescape(cf['value'])

      m_data['bank_account_type'] = 'iban'
      m_data['lang'] = 'ca_ES'
      m_data['name'] = h.unescape(wp_member.title)

      if m_data['company_type'] == 'company':
        m_data['representative_dni'] = m_data['dni']
        m_data.pop('dni', None)

      return {
        'm_data': m_data,
        'cs_registration': cs_registration
      }
    return False
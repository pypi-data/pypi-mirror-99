from html.parser import HTMLParser
from datetime import datetime
from odoo.addons.sm_maintenance.models.models_sm_utils import sm_utils
from odoo.addons.sm_connect.models.models_sm_wordpress_db_utils import sm_wordpress_db_utils

class sm_reward_utils(object):

  __instance = None

  @staticmethod
  def get_instance():
    if sm_reward_utils.__instance is None:
      sm_reward_utils()
    return sm_reward_utils.__instance

  def __init__(self):
    if sm_reward_utils.__instance is not None:
      raise Exception("This class is a singleton!")
    else:
      sm_reward_utils.__instance = self

  def complete_rewards(self, parent):
    rewards = parent.env['sm_rewards.sm_reward'].search([
      ('final_state', '=', 'not_completed'),
      ('reward_type', '=', 'promocode')
    ])
    if rewards.exists():
      for reward in rewards:
        reward.complete_process()

  def fetch_wp_rewards(self, parent):
    self._fetch_reward_members(parent)
    self._fetch_reward_member_coupons(parent)
    self._fetch_reward_maintenance(parent)

  def _fetch_reward_members(self,parent):
    members = parent.env['res.partner'].search([], order='id desc')  # TODO search by condition
    if members.exists():
      for member in members:
        if member.creation_coupon:
          if self._coupon_index_must_create_system_reward(parent,member.creation_coupon):
            self._create_if_must_system_reward_from_wp_member_id(parent,member.wp_member_id)

  def _fetch_reward_maintenance(self,parent):
    db_utils = sm_wordpress_db_utils.get_instance()
    maintenances = db_utils.get_feedback_caldera('CF5d25a01da742f')
    for entry_id in maintenances.keys():
      existing_reward = parent.env['sm_rewards.sm_reward'].search([('maintenance_wp_entry_id', '=', entry_id)])
      if not existing_reward.exists():
        parsed_data = self._parse_wp_maintenance_data_for_system_reward(parent,entry_id,maintenances[entry_id])
        if parsed_data:
          new_reward = parent.env['sm_rewards.sm_reward'].create(parsed_data)

  def _fetch_reward_member_coupons(self,parent):
    db_utils = sm_wordpress_db_utils.get_instance()
    mcargs = {
      'post_type': 'sm_member_coupon',
      'orderby': 'ID',
      'order': 'DESC',
      'number': 500
    }
    wp_member_coupons = db_utils.get_posts(mcargs)
    if wp_member_coupons:
      for wp_member_coupon in wp_member_coupons:
        self._create_if_must_system_reward_from_wp_member_coupon(parent,wp_member_coupon)


  def _create_if_must_system_reward_from_wp_member_id(self,parent, wp_member_id):
    db_utils = sm_wordpress_db_utils.get_instance()
    wp_member = db_utils.get_post_by_id(wp_member_id)
    if wp_member:
      if self._wp_member_must_create_system_reward(wp_member):
        m_data = self._parse_wp_member_data_for_system_reward(parent, wp_member)
        if m_data:
          parent.env['sm_rewards.sm_reward'].create(m_data)
          return True
    return False

  def _create_if_must_system_reward_from_wp_member_coupon(self,parent,wp_member_coupon):
    if wp_member_coupon:
      m_data = self._parse_wp_member_coupon_data_for_system_reward(parent,wp_member_coupon)
      if m_data:
        existing_reward = rewards = parent.env['sm_rewards.sm_reward'].search([
          ('wp_member_coupon_id', '=', m_data['wp_member_coupon_id'])
        ])
        if not rewards.exists():
          if 'promo_code' in m_data.keys():
            if self._coupon_index_must_create_system_reward(parent,m_data['promo_code']):
              parent.env['sm_rewards.sm_reward'].create(m_data)
              return True


  def _coupon_index_must_create_system_reward(self,parent,coupon_index):
    existing_reward = parent.env['sm_rewards.sm_reward'].search(
      [('promo_code', '=', coupon_index)], order='id desc')
    existing_not_found = parent.env['sm_rewards.sm_reward'].search(
      [('promo_code', '=', coupon_index), ('final_state', '=', 'soci_not_found')],
      order='id desc')
    existing_diff_not_found = parent.env['sm_rewards.sm_reward'].search(
      [('promo_code', '=', coupon_index), ('final_state', '!=', 'soci_not_found')],
      order='id desc')
    # (not existing reward) or (exists not found + not newly created)
    if not existing_reward.exists() or (existing_not_found.exists() and not existing_diff_not_found.exists()):
      return True
    return False

  def _wp_member_must_create_system_reward(self, wp_member):
    if wp_member:
      for custom_field in wp_member.custom_fields:
        if custom_field['key'] == 'member_details_coupon':
          if custom_field['value'] != '':
            return True
        if custom_field['key'] == 'member_details_pocketbook':
          if custom_field['value'] != '' and custom_field['value'] != '0':
            return True
        if custom_field['key'] == 'member_details_pocketbook_money':
          if custom_field['value'] != '' and custom_field['value'] != '0':
            return True
    return False

  def _wp_member_id_must_create_system_reward(self,wp_member_id):
    if wp_member_id:
      db_utils = sm_wordpress_db_utils.get_instance()
      wp_member = db_utils.get_post_by_id(wp_member_id)
      if wp_member:
        return self._wp_member_must_create_system_reward(wp_member)
    return False

  def _parse_wp_maintenance_data_for_system_reward(self,parent,entry_id,data):
    if data:
      srd = {'maintenance_wp_entry_id': entry_id}
      srd['user_dni'] = self._setup_dict_entry(data,'member_dni')
      srd['reward_date'] = self._setup_dict_entry(data,'data')
      srd['maintenance_reservation_type'] = self._setup_dict_entry(data,'tipus_de_reserva')
      srd['maintenance_type'] = self._setup_dict_entry(data,'tasques_manteniment')
      srd['maintenance_duration'] = self._setup_dict_entry(data,'duraci_de_la_tasca')
      srd['maintenance_observations'] = self._setup_dict_entry(data,'voldries_comentar_alguna_cosa_ms_si_has_marcat_altres_indica_aqu_la_tasca')
      srd['maintenance_carconfig_index'] = self._setup_dict_entry(data,'cs_feedback_car_id')
      srd['maintenance_carconfig_home'] = self._setup_dict_entry(data,'cs_feedback_home')
      srd['maintenance_cs_person_index'] = self._setup_dict_entry(data,'cs_feedback_member_id')
      srd['maintenance_reservation_start'] = self._setup_dict_entry(data,'cs_feedback_reservation_start')
      srd['maintenance_car_plate'] = self._setup_dict_entry(data,'car_plate')

      srd['reward_type'] = 'fleet_maintenance'

      srd['name'] = "Maintenance: "+ str(entry_id)
      srd['reward_info'] = srd['name']

      if srd['maintenance_reservation_start']:
        srd['maintenance_reservation_start'] = str(srd['maintenance_reservation_start'])+"000"
        try:
          date_obj = datetime.strptime(srd['maintenance_reservation_start'], "%Y-%m-%dT%H:%M:%S.%f")
        except:
          date_obj = False
        if date_obj:
          srd['maintenance_reservation_start'] = date_obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
          srd['maintenance_reservation_start'] = False

      if srd['reward_date']:
        try:
          date_obj = datetime.strptime(srd['reward_date'], "%d/%m/%Y")
        except:
          date_obj = False
        if date_obj:
          srd['reward_date'] = date_obj.strftime("%Y-%m-%d")
        else:
          srd['reward_date'] = False

      if srd['maintenance_reservation_type'] == 'maintenace':
        srd['maintenance_forgive_reservation'] = True
      if srd['maintenance_reservation_type'] == 'reservation_and_maintenance':
        srd['maintenance_discount_reservation'] = True

      if srd['maintenance_duration'] != 'other':
        if srd['maintenance_duration']:
          srd['reward_addtime'] = int(srd['maintenance_duration'])
          # TODO: reward price must be edited on config
          srd['reward_addmoney'] = float(srd['maintenance_duration'])*0.25

      srd['maintenance_create_car_service'] = False
      service_query = False
      aa_query = False
      # TODO: This equivalence must be defined on a config table.
      if srd['maintenance_type'] != 'other':
        if srd['maintenance_type'] == 'clean_outside':
          srd['maintenance_create_car_service'] = True
          aa_query = "Recompenses Neteja"
          service_query = 'Neteja - Exterior'
        if srd['maintenance_type'] == 'clean_inside':
          srd['maintenance_create_car_service'] = True
          aa_query = "Recompenses Neteja"
          service_query = 'Neteja - Interior'
        if srd['maintenance_type'] == 'clean_inside_outside':
          srd['maintenance_create_car_service'] = True
          aa_query = "Recompenses Neteja"
          service_query = 'Neteja - Interior / Exterior'
        if srd['maintenance_type'] == 'wheel_pressure':
          srd['maintenance_create_car_service'] = True
          aa_query = "Recompenses manteniment"
          service_query = 'Manteniment - Ajustar pressió rodes'
        if srd['maintenance_type'] == 'car_to_mechanic':
          srd['maintenance_create_car_service'] = False
          aa_query = "Recompenses logística cotxes"
        if srd['maintenance_type'] == 'swap_car':
          srd['maintenance_create_car_service'] = False
          aa_query = "Recompenses logística cotxes"
        if srd['maintenance_type'] == 'charge_car':
          srd['maintenance_create_car_service'] = False
          aa_query = "Recompenses logística cotxes"
        if srd['maintenance_type'] == 'member_tutorial':
          srd['maintenance_create_car_service'] = False
          aa_query = "Feines tècniques i consultoria"
        if srd['maintenance_type'] == 'representation_act':
          srd['maintenance_create_car_service'] = False
          aa_query = "Feines tècniques i consultoria"

      if service_query:
        st = parent.env['fleet.service.type'].search([('name', '=', service_query)])
        if st.exists():
          srd['maintenance_car_service_id'] = st[0].id

      if aa_query:
        a_account = parent.env['account.analytic.account'].search([('name', '=', aa_query)])
        if a_account.exists():
          srd['related_analytic_account_id'] = a_account[0].id


      if srd['maintenance_reservation_start'] and srd['maintenance_carconfig_index']:
        existing_cc = parent.env['smp.sm_car_config'].search([('name','=',srd['maintenance_carconfig_index'])])
        if existing_cc.exists():
          existing_r = parent.env['smp.sm_reservation_compute'].search([
            ('carconfig_id','=',existing_cc[0].id),
            ('startTimechar','=',srd['maintenance_reservation_start'])
          ])
          if existing_r.exists():
            srd['maintenance_reservation_id'] = existing_r[0].id

      return srd

    return False

  def _setup_dict_entry(self,data,key):
    try:
      ret = data[key]
    except:
      ret = False
    return ret

  def _parse_wp_member_coupon_data_for_system_reward(self,parent,wp_member_coupon):
    if wp_member_coupon:
      h = HTMLParser()
      m_data = {}
      mcm = wp_member_coupon.custom_fields
      for custom_field in mcm:
        if custom_field['key'] == 'member_coupon_pocketbook':
          m_data['reward_addtime'] = custom_field['value']
        if custom_field['key'] == 'member_coupon_pocketbook_money':
          m_data['reward_addmoney'] = custom_field['value']
        if custom_field['key'] == 'member_coupon_member_dni':
          m_data['user_dni'] = custom_field['value'].upper().strip()
        if custom_field['key'] == 'member_coupon_reward_group_config':
          m_data['group_config'] = custom_field['value']
        if custom_field['key'] == 'member_coupon_coupon':
          m_data['promo_code'] = str(custom_field['value']).upper().strip()
        if custom_field['key'] == 'member_coupon_email':
          m_data['member_email'] = custom_field['value']
        if custom_field['key'] == 'member_coupon_reward_info':
          m_data['reward_info'] = custom_field['value']
        if custom_field['key'] == 'member_coupon_force_cs_registration':
          if custom_field['value']:
              m_data['force_register_cs'] = False
              if custom_field['value'] == '1':
                m_data['force_register_cs'] = True
        if custom_field['key'] == 'member_coupon_cs_dedicated_ba':
          if custom_field['value']:
              m_data['force_dedicated_ba'] = False
              if custom_field['value'] == '1':
                m_data['force_dedicated_ba'] = True
        if custom_field['key'] == 'member_coupon_tariff_name':
          m_data['tariff_name'] = custom_field['value']
        if custom_field['key'] == 'member_coupon_tariff_related_model':
          m_data['tariff_related_model'] = custom_field['value']
        if custom_field['key'] == 'member_coupon_tariff_type':
          m_data['tariff_type'] = custom_field['value']
        if custom_field['key'] == 'member_coupon_tariff_quantity':
          m_data['tariff_quantity'] = custom_field['value']
        if custom_field['key'] == 'member_coupon_group':
          m_data['coupon_group'] = custom_field['value']
        if custom_field['key'] == 'member_coupon_secondary_group':
          m_data['coupon_group_secondary'] = custom_field['value']
        if custom_field['key'] == 'member_coupon_id':
          m_data['wp_coupon_id'] = custom_field['value']
        if custom_field['key'] == 'member_coupon_reward_analytic_account':
          a_account = parent.env['account.analytic.account'].search([('name', '=', custom_field['value'])])
          if a_account.exists():
            m_data['related_analytic_account_id'] = a_account[0].id

      if bool(m_data):
          m_data['wp_member_coupon_id'] = wp_member_coupon.id
          m_data['member_name'] = h.unescape(wp_member_coupon.title)
          m_data['name'] = m_data['member_name'] + " - " + m_data['reward_info']
          m_data['reward_type'] = 'promocode'
          m_data['reward_date'] = wp_member_coupon.date
          return m_data
      return False

  def _parse_wp_member_data_for_system_reward(self,parent, wp_member):
    if wp_member:
      h = HTMLParser()
      m_data = {}
      for custom_field in wp_member.custom_fields:
        # coupon data
        if custom_field['key'] == 'member_details_coupon':
          if custom_field['value'] != '':
            m_data['promo_code'] = custom_field['value']

        if custom_field['key'] == 'member_details_coupon_id':
          m_data['wp_coupon_id'] = custom_field['value']

        # reward
        if custom_field['key'] == 'member_details_reward_info':
          if custom_field['value'] != '':
            m_data['reward_info'] = custom_field['value']

        if custom_field['key'] == 'member_details_pocketbook':
          if custom_field['value'] != '' and custom_field['value'] != '0':
            m_data['reward_addtime'] = custom_field['value']

        if custom_field['key'] == 'member_details_pocketbook_money':
          if custom_field['value'] != '' and custom_field['value'] != '0':
            m_data['reward_addmoney'] = custom_field['value']

        # member data
        if custom_field['key'] == 'member_details_dni':
          if custom_field['value'] != '' and custom_field['value'] != '0':
            m_data['user_dni'] = custom_field['value']
        if custom_field['key'] == 'member_details_email':
          if custom_field['value'] != '':
            m_data['member_email'] = custom_field['value']

        # cs data
        if custom_field['key'] == 'member_details_force_cs_registration':
          if custom_field['value']:
              m_data['force_register_cs'] = False
              if custom_field['value'] == '1':
                m_data['force_register_cs'] = True
        if custom_field['key'] == 'member_details_cs_dedicated_ba':
          if custom_field['value']:
              m_data['force_dedicated_ba'] = False
              if custom_field['value'] == '1':
                m_data['force_dedicated_ba'] = True

        if custom_field['key'] == 'member_details_reward_group_config':
          if custom_field['value'] != '':
            m_data['group_config'] = custom_field['value']
        if custom_field['key'] == 'member_details_reward_group':
          if custom_field['value'] != '':
            m_data['coupon_group'] = custom_field['value']
        if custom_field['key'] == 'member_details_reward_secondary_group':
          if custom_field['value'] != '':
            m_data['coupon_group_secondary'] = custom_field['value']

        # reward tariff creation data
        if custom_field['key'] == 'member_details_tariff_name':
          m_data['tariff_name'] = custom_field['value']
        if custom_field['key'] == 'member_details_tariff_related_model':
          m_data['tariff_related_model'] = custom_field['value']
        if custom_field['key'] == 'member_details_tariff_type':
          m_data['tariff_type'] = custom_field['value']
        if custom_field['key'] == 'member_details_tariff_quantity':
          m_data['tariff_quantity'] = custom_field['value']

        # analytic account
        if custom_field['key'] == 'member_details_reward_analytic_account':
          a_account = parent.env['account.analytic.account'].search([('name','=',custom_field['value'])])
          if a_account.exists():
            m_data['related_analytic_account_id'] = a_account[0].id

      if bool(m_data):
        m_data['wp_member_id'] = wp_member.id
        m_data['member_name'] = h.unescape(wp_member.title)
        m_data['name'] = m_data['member_name']
        if 'reward_info' in m_data.keys():
          m_data['name'] += " - " + m_data['reward_info']
        m_data['reward_type'] = 'promocode'
        m_data['reward_date'] = wp_member.date
        return m_data
    return False
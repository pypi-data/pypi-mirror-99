# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from html.parser import HTMLParser
from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.addons.sm_maintenance.models.models_sm_utils import sm_utils
from odoo.addons.sm_maintenance.models.models_sm_resources import sm_resources
from odoo.addons.sm_connect.models.models_sm_wordpress_db_utils import sm_wordpress_db_utils

class sm_reward(models.Model):
  _name = 'sm_rewards.sm_reward'
  _inherit = ['mail.thread']
  _description = "CS Reward"

  name = fields.Char(string=_("Name"))
  member_name = fields.Char(string=_("Member name"))
  member_email = fields.Char(string=_("Member email"))
  user_dni = fields.Char(string=_("Dni"))
  related_member_id = fields.Many2one('res.partner', string=_("Partner"))
  related_analytic_account_id = fields.Many2one(
    'account.analytic.account', string=_("Reward analytic account"))

  promo_code = fields.Char(string=_("Promo code"))
  wp_coupon_id = fields.Char(string=_("Coupon wp ID"))
  wp_member_id = fields.Char(string=_("Member wp ID"))
  wp_member_coupon_id = fields.Char(string=_("Member coupon wp ID"))

  reward_date = fields.Date(string=_("Date"))
  reward_addtime = fields.Integer(string=_("Reward (time/minutes)"))
  reward_addmoney = fields.Float(string=_("Reward (money)"))
  reward_type = fields.Selection([
    ('promocode', 'Promo codes'),
    ('fleet_maintenance', 'Fleet maintenance')], string=_("Type"),required=True)
  reward_info = fields.Char(string=_("Info"))
  # reward_register_cs = fields.Boolean(string=_("Register in carsharing"))

  completed = fields.Date(string=_("Completed Date"))

  # TODO: To be removed
  group_config = fields.Char(string=_("Group config"))
  
  coupon_group = fields.Char(string=_("Group (index)"))
  coupon_group_secondary = fields.Char(string=_("Secondary Group (index)"))

  tariff_name = fields.Char(string=_("Tariff Name"))
  tariff_related_model = fields.Char(string=_("Related model"))
  tariff_type = fields.Char(string=_("Type"))
  tariff_quantity = fields.Char(string=_("Quantity"))

  force_register_cs = fields.Boolean(string=_("Force registration"))
  force_dedicated_ba = fields.Boolean(string=_("Force dedicated billingAccount"))

  state = fields.Selection([
    ('new', 'New'),
    ('member','Member computed'),
    ('follower','Follower added'),
    ('complete', 'Completed')
  ], default='new')

  final_state = fields.Selection([
    ('not_completed', 'Not completed'),
    ('soci_not_found', 'Member not found'),
    ('reward_completed', 'Completed')
  ], default='not_completed')

  # MAINTENANCE FIELDS
  maintenance_reservation_type = fields.Selection([
    ('maintenace', 'Reservation only for maintenance task'),
    ('reservation_and_maintenance', 'Reservation and maintenance task'),
  ],string=_("Maintenance reservation type"))
  maintenance_forgive_reservation = fields.Boolean(string=_("Forgive related reservation"))
  maintenance_type = fields.Selection([
    ('clean_inside', 'Clean inside vehicle'),
    ('clean_outside', 'Clean outside vehicle'),
    ('clean_inside_outside', 'Clean inside and outside vehicle'),
    ('car_to_mechanic', 'Bring car to mechanic'),
    ('swap_car', 'Swap car'),
    ('wheel_pressure', 'Adjust wheel pressure'),
    ('charge_car', 'Charge vehicle'),
    ('member_tutorial', 'Teach another member'),
    ('representation_act', 'Representation act'),
    ('other', 'Other'),
  ],string=_("Maintenance type"))
  maintenance_duration = fields.Char(string=_("Maintenance duration"))
  maintenance_observations = fields.Text(string=_("Observations"))
  maintenance_carconfig_index = fields.Char(string=_("carConfig index"))
  maintenance_carconfig_id = fields.Many2one('smp.sm_car_config',string=_("carConfig DB"),
    compute="_get_maintenance_carconfig_id",store=True)
  maintenance_carconfig_home = fields.Char(string=_("carConfig Home"))
  maintenance_cs_person_index = fields.Char(string=_("Carsharing person index"))
  maintenance_reservation_start = fields.Char(string=_("Reservation start"))
  maintenance_reservation_id = fields.Many2one('smp.sm_reservation_compute',string=_("Reservation DB"))
  maintenance_car_plate = fields.Char(string=_("Car plate (from form)"))
  maintenance_car_id = fields.Many2one('fleet.vehicle',string=_("car DB"),
    compute="_get_maintenance_car_id",store=True)
  maintenance_car_id_plate = fields.Char(string="car License plate",compute="_get_maintenance_car_id_plate")
  maintenance_create_car_service = fields.Boolean(string=_("Create car service"))
  maintenance_car_service_id = fields.Many2one('fleet.service.type',string=_("car service DB"))
  maintenance_discount_reservation = fields.Boolean(string=_("Discount minutes from reservation"))

  maintenance_wp_entry_id = fields.Char("Maintenance wp ID")

  maintenance_car_service_log_ids = fields.One2many(
    comodel_name ='fleet.vehicle.log.services',
    inverse_name='related_reward_id',
    string=_("CS car services"))
  
  cs_registration_request_ids = fields.One2many(
    comodel_name ='sm_partago_user.carsharing_registration_request',
    inverse_name='related_reward_id',
    string=_("CS registration requests"))

  pb_record_ids = fields.One2many(
    comodel_name ='pocketbook.pocketbook_record',
    inverse_name='related_reward_id',
    string=_("CS pocketbook records"))

  tariffs_ids = fields.One2many(
    comodel_name ='smp.sm_carsharing_tariff',
    inverse_name='related_reward_id',
    string=_("CS tariffs"))

  _order = "reward_date desc"

  # COMPUTED FIELDS
  @api.depends('maintenance_carconfig_index')
  def _get_maintenance_carconfig_id(self):
    for record in self:
      if record.maintenance_carconfig_index:
        existing_cc = self.env['smp.sm_car_config'].search([('name','=',record.maintenance_carconfig_index)])
        if existing_cc.exists():
          record.maintenance_carconfig_id = existing_cc[0].id

  @api.depends('maintenance_carconfig_id','maintenance_car_plate')
  def _get_maintenance_car_id(self):
    for record in self:
      lp = False
      if record.maintenance_carconfig_id:
        lp = record.maintenance_carconfig_id.rel_car_id_license_plate
      else:
        if record.maintenance_car_plate:
          lp = record.maintenance_car_plate
      if lp:
        existing_c = self.env['fleet.vehicle'].search([('license_plate','=',lp)])
        if existing_c.exists():
          record.maintenance_car_id = existing_c[0].id

  @api.depends('maintenance_car_id')
  def _get_maintenance_car_id_plate(self):
    for record in self:
      if record.maintenance_car_id:
        record.maintenance_car_id_plate = record.maintenance_car_id.license_plate

  # MODEL ACTIONS
  @api.multi
  def completed_progressbar_action(self):
    if self.state == 'follower':
      validation = self._validate_completion()
      if validation['valid']:
        self.complete_process()
      else:
        resources = sm_resources.getInstance()
        return resources.get_successful_action_message(self,validation['error'], self._name)

  @api.multi
  def member_progressbar_action(self):
    if self.state == 'new':
      fetch_success = self.fetch_user()
      if fetch_success:
        self.set_status('member')
      else:
        resources = sm_resources.getInstance()
        return resources.get_successful_action_message(self,
        _('Error: Member not found'), self._name)

  @api.multi
  def follower_progressbar_action(self):
    if self.state == 'member':
      follower_success = self.add_follower()
      if follower_success:
        self.set_status('follower')
      else:
        resources = sm_resources.getInstance()
        return resources.get_successful_action_message(self,
        _("Error: Couldn't add follower to reward"), self._name)

  def set_status(self,status):
    self.write({
      'state': status
    })

  def set_complete_status(self, final_state='reward_completed'):
    self.write({
      'state': 'complete',
      'final_state': final_state,
      'completed': datetime.now()
    })

  def reset_state_action(self):
    if self.env.context:
      rwds = self.env['sm_rewards.sm_reward'].browse(
        self.env.context['active_ids'])
      if rwds.exists():
        for rwd in rwds:
          rwd.write({
            'state': 'new',
            'final_state': 'not_completed',
            'completed': False
          })

  def _validate_completion(self):
    if self.maintenance_create_car_service:
      if not self.maintenance_car_id or not self.maintenance_car_service_id:
        return {
          'error': _("Error: Not enough fields for car service."),
          'valid': False
        }
    if self.maintenance_forgive_reservation:
      if not self.maintenance_reservation_id:
        return {
          'error': _("Error: No related reservation to fotgive."),
          'valid': False
        }
    if self.maintenance_discount_reservation:
      if not self.maintenance_reservation_id or self.reward_addtime == 0 or not self.reward_addtime:
        return {
          'error': _("Error: Trying to discount time in reservation. No reservation or no time to discount"),
          'valid': False
        }

    if not self.related_analytic_account_id:
      return {
        'error': _("Error: No analytic account."),
        'valid': False
      }
    return {
      'valid': True
    }

  def add_follower(self):
    if self.related_member_id:
      self.message_subscribe([self.related_member_id.id])
      return True
    return False

  # MEMBER COMPUTE
  def fetch_user_error(self, rwd=None):
    db_utils = sm_wordpress_db_utils.get_instance()
    if rwd is None:
      rwd = self
    if rwd.wp_coupon_id:
      db_utils.reactivate_coupon(rwd)
    rwd.set_complete_status('soci_not_found')
    sm_utils.send_email_from_template(
      rwd, 'cs_reward_soci_not_found_email_template_id')

  def fetch_user(self, rwd=None):
    h = HTMLParser()
    if rwd is None:
      rwd = self
    if rwd.maintenance_cs_person_index:
      rel_member_q = self.env['res.partner'].sudo().search([('cs_person_index', '=', rwd.maintenance_cs_person_index)])
      if rel_member_q.exists():
        rwd.write({
          'related_member_id': rel_member_q[0].id
        })
        return True
    else:
      if rwd.user_dni:
        q = str(rwd.user_dni).replace("-", "").replace(" ", "").upper()
        rel_member_q = self.env['res.partner'].sudo().search([('dni', '=', q)])
        if rel_member_q.exists():
          email_r_member_found = False
          for rmember in rel_member_q:
            if rmember.email == self.member_email:
              rwd.write({
                'related_member_id': rmember.id
              })
              email_r_member_found = True
              break
          if not email_r_member_found:
            rwd.write({
              'related_member_id': rel_member_q[0].id
            })
          return True
    return False

  # POCKETBOOK
  def register_new_pocketbook_record_if_must(self, rwd):
    if rwd.reward_addmoney > 0:
      company = self.env.user.company_id
      pb_account = company.reward_account_id.id
      pb_analytic_account = company.reward_analytic_account_id.id
      if rwd.related_analytic_account_id.id != False:
        pb_analytic_account = rwd.related_analytic_account_id.id
      # TODO: This naming must go to config table / DB
      pb_record_name = _("Recompensa")
      if rwd.reward_type == 'promocode':
        pb_record_name = pb_record_name + ": " + rwd.promo_code
      if rwd.reward_type == 'fleet_maintenance' and rwd.related_analytic_account_id:
        pb_record_name = rwd.related_analytic_account_id.name
        if rwd.related_analytic_account_id.name == 'Feines tècniques i consultoria':
          pb_record_name = 'Recompensa: Som Mobilitat'
      new_pb_record = self.env['pocketbook.pocketbook_record'].create({
        'name': pb_record_name,
        'date': datetime.now().strftime("%Y-%m-%d"),
        'obs': "reward id: "+ str(rwd.id),
        'related_member_id': rwd.related_member_id.id,
        'related_account_id': pb_account,
        'related_analytic_account_id': pb_analytic_account,
        'related_reward_id': rwd.id
      })
      new_pb_record_history = self.env['pocketbook.pocketbook_record_history'].create({
        'name': _("Reward: ") + rwd.reward_type,
        'date': datetime.now().strftime("%Y-%m-%d"),
        'amount': rwd.reward_addmoney / 1.21,
        'related_pb_record_id': new_pb_record.id
      })

  # TARIFF
  def must_create_user_tariff(self):
    if self.tariff_name and self.tariff_related_model and self.tariff_type and self.tariff_quantity:
      return True
    return False

  def create_new_user_tariff_if_must(self):
    if self.must_create_user_tariff():
      sys_date = sm_utils.get_today_date()
      related_tariff_model = self.env['smp.sm_carsharing_tariff_model'].search([
        ("name", "=", self.tariff_related_model)
      ])
      if related_tariff_model.exists():
        self.env['smp.sm_carsharing_tariff'].create({
          "name": self.tariff_name,
          "related_member_id": self.related_member_id.id,
          "tariff_model_id": related_tariff_model[0].id,
          "tariff_type": self.tariff_type,
          "pocketbook": self.tariff_quantity,
          "pocketbook_initial": self.tariff_quantity,
          "date": sys_date,
          "date_active": sys_date,
          'related_reward_id': self.id
        })

  def complete_process(self, rwd=None):
    if rwd is None:
      rwd = self
    if rwd.final_state == "not_completed":
      if not rwd.related_member_id:
        rwd.fetch_user()
      if rwd.related_member_id:
        
        # CREATE SERVICE
        if rwd.maintenance_create_car_service:
          if rwd.maintenance_car_id and rwd.maintenance_car_service_id:
            if rwd.reward_date:
              rd = rwd.reward_date
            else:
              rd = datetime.now()
            self.env['fleet.vehicle.log.services'].create({
              'vehicle_id': rwd.maintenance_car_id.id,
              'cost_subtype_id': rwd.maintenance_car_service_id.id,
              'amount': float(rwd.reward_addmoney),
              'date': rd,
              'related_reward_id': rwd.id,
              'related_member_id': rwd.related_member_id.id
            })
          else:
            error_msg = _("""CS Reward car service error. Not all fields for service. Reward id: %s""") % (str(rwd.id))
            sm_utils.create_system_task(self,"CS Reward Car service error.",error_msg)

        # FORGIVE RESERVATION
        if rwd.maintenance_forgive_reservation:
          if rwd.maintenance_reservation_id:
            rwd.maintenance_reservation_id.write({
              'compute_forgiven': True
            })
          else:
            error_msg = _("""CS Reward forgive reservation error. No related reservation. Reward id: %s""") % (str(rwd.id))
            sm_utils.create_system_task(self,"CS Reward forgive reservation error.",error_msg)

        # DISCOUNT RESERVATION
        if rwd.maintenance_discount_reservation:
          if rwd.maintenance_reservation_id and rwd.reward_addtime:
            r_start_time = datetime.strptime(
                rwd.maintenance_reservation_id.startTime, "%Y-%m-%d %H:%M:%S")
            r_effective_start_time = datetime.strptime(
                rwd.maintenance_reservation_id.effectiveStartTime, "%Y-%m-%d %H:%M:%S")
            r_effective_end_time = datetime.strptime(
                rwd.maintenance_reservation_id.effectiveEndTime, "%Y-%m-%d %H:%M:%S")
            r_effective_end_time_discount = r_effective_end_time + timedelta(minutes=-1*rwd.reward_addtime)
            if r_effective_end_time_discount > r_effective_start_time and r_effective_end_time_discount > r_start_time:
              rwd.maintenance_reservation_id.write({
                'effectiveEndTime': r_effective_end_time_discount,
                'ignore_update': True
              })
            else:
              error_msg = _("""CS Reward discount reservation error. Too much discount. Reward id: %s""") % (str(rwd.id))
              sm_utils.create_system_task(self,"CS Reward discount reservation error.",error_msg)
          else:
            error_msg = _("""CS Reward discount reservation error. No related reservation. Reward id: %s""") % (str(rwd.id))
            sm_utils.create_system_task(self,"CS Reward discount reservation error.",error_msg)

        # COMPUTE REWARD
        company_error = False
        # 1.- Company user pass reward to company
        if rwd.related_member_id.cs_user_type == 'organisation':
          if rwd.related_member_id.parent_id:
            rwd.write({
              'related_member_id': rwd.related_member_id.parent_id.id
            })
          else:
            error_msg = _("""CS Reward Company error. Company not found for company user. Reward id: %s""") % (str(rwd.id))
            sm_utils.create_system_task(self,"CS company user error.",error_msg)
            company_error = True
        if not company_error:
          create_registration_request = True
          # 2.- Complete reward
          if self.force_dedicated_ba:
            # 2.1.- dedicated ba
            ba_behaviour = 'dedicated_ba'
          else:
            # 2.2.- Regular users and maintenance
            if rwd.related_member_id.cs_user_type in ['user','maintenance']:
              rwd.register_new_pocketbook_record_if_must(rwd)
              rwd.create_new_user_tariff_if_must()
              ba_behaviour = 'no_ba'
              if rwd.related_member_id.cs_state in ['blocked_banned','active'] \
              and rwd.reward_type == 'fleet_maintenance' \
              and not rwd.coupon_group:
                create_registration_request = False
            # 2.3.- cs users
            else:
              ba_behaviour = 'update_ba'
          
          # 3.- Registration only for persons
          if rwd.related_member_id.company_type == 'person' and create_registration_request:
            self._create_registration_request(
              rwd,
              rwd.coupon_group,
              ba_behaviour,
              rwd.reward_addtime
            )
            if rwd.coupon_group_secondary:
              if rwd.coupon_group_secondary != '':
                # TODO: We impose secondary group for dedicated_ba enters in normal payment group (no promo) need to make this dynamic
                if ba_behaviour == 'dedicated_ba':
                  ba_behaviour = 'no_ba'
                self._create_registration_request(
                  rwd,
                  rwd.coupon_group_secondary,
                  ba_behaviour,
                  0
                )

        if rwd.reward_addmoney > 0 or rwd.reward_addtime > 0:
          if self.reward_type == 'promocode':
            # TODO: This must be a configuration field on the model (send_completed_email_to_user)
            if self.reward_info != 'promo Montepio':
              sm_utils.send_email_from_template(rwd, 'cs_reward_completed_email_template_id')

        rwd.set_complete_status('reward_completed')

      else:
        # soci not found
        rwd.fetch_user_error()

  def _create_registration_request(self, rwd, group_index,ba_behaviour,ba_credits):
    self.env['sm_partago_user.carsharing_registration_request'].create({
      'related_member_id': rwd.related_member_id.id,
      'force_registration': rwd.force_register_cs,
      'group_index': group_index,
      'ba_behaviour': ba_behaviour,
      'ba_credits': ba_credits,
      'related_coupon_index': rwd.promo_code,
      'related_reward_id': rwd.id
    })

  # OBS: use only for migration purposes
  def sanitize_reward_db_action(self):
    db_utils = sm_wordpress_db_utils.get_instance()
    if self.env.context:
      rwds = self.env['sm_rewards.sm_reward'].browse(
        self.env.context['active_ids'])
      if rwds.exists():
        for rwd in rwds:
          rwd.fetch_user()
          rwd.set_complete_status()

  #         if rwd.final_state == 'not_completed':
  #           rwd.set_complete_status()
  #   WP COUPON ID
  #   mcargs = {
  #     'post_type': 'sm_coupon',
  #     'orderby': 'ID',
  #     'order': 'DESC'
  #   }
  #   # get pages in batches of 20
  #   offset = 0
  #   increment = 100
  #   coupon_found = False
  #   while coupon_found == False:
  #     mcargs['number'] = increment
  #     mcargs['offset'] = offset
  #     member_coupons = db_utils.get_posts(mcargs)
  #     if len(member_coupons) == 0:
  #       break  # no more posts returned
  #     for wp_member_coupon in member_coupons:
  #       rewards = self.env['sm_rewards.sm_reward'].search([
  #         ('promo_code', '=', wp_member_coupon.title)
  #       ])
  #       if rewards.exists():
  #         for reward in rewards:
  #           if not reward.wp_coupon_id:
  #             reward.write({
  #               'wp_coupon_id': wp_member_coupon.id
  #             })
  #     offset = offset + increment

  #   # WP MEMBER COUPON ID 
  #   mcargs = {
  #     'post_type': 'sm_member_coupon',
  #     'orderby': 'ID',
  #     'order': 'DESC',
  #     'number': 500
  #   }
  #   wp_member_coupons = db_utils.get_posts(mcargs)
  #   if wp_member_coupons:
  #     for wp_member_coupon in wp_member_coupons:
  #       existing_rewards = rewards = self.env['sm_rewards.sm_reward'].search([
  #         ('wp_member_coupon_id', '=', wp_member_coupon.id)
  #       ])
  #       if not existing_rewards.exists():
  #         for custom_field in wp_member_coupon.custom_fields:
  #           if custom_field['key'] == 'member_coupon_coupon' and custom_field['value'] != '':
  #             rewards = self.env['sm_rewards.sm_reward'].search([
  #               ('promo_code', '=', str(custom_field['value']).upper().strip())
  #             ])
  #             if rewards.exists():
  #               for reward in rewards:
  #                 if not reward.wp_member_id:
  #                   reward.write({
  #                     'wp_member_coupon_id': wp_member_coupon.id
  #                   })
  #   # WP_MEMBER
  #   mcargs = {
  #     'post_type': 'sm_member',
  #     'orderby': 'ID',
  #     'order': 'DESC'
  #   }
  #   # get pages in batches of 100
  #   offset = 0
  #   increment = 100
  #   coupon_found = False
  #   while coupon_found == False:
  #     mcargs['number'] = increment
  #     mcargs['offset'] = offset
  #     member_coupons = db_utils.get_posts(mcargs)
  #     if len(member_coupons) == 0:
  #       break  # no more posts returned
  #     for wp_member_coupon in member_coupons:
  #       for custom_field in wp_member_coupon.custom_fields:
  #         if custom_field['key'] == 'member_details_coupon' and custom_field['value'] != '':
  #           rewards = self.env['sm_rewards.sm_reward'].search([
  #             ('promo_code', '=', str(custom_field['value']).upper().strip())
  #           ])
  #           if rewards.exists():
  #             for reward in rewards:
  #               if not reward.wp_member_coupon_id:
  #                 reward.write({
  #                   'wp_member_id': wp_member_coupon.id
  #                 })
  #     offset = offset + increment
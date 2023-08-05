# -*- coding: utf-8 -*-
from html.parser import HTMLParser

from odoo import models, api

from odoo.addons.sm_rewards.models.models_sm_reward_utils import sm_reward_utils


class sm_reward_fetch_wizard(models.TransientModel):
  _name = "sm_rewards.sm_reward_fetch_wizard"

  @api.multi
  def create_request(self):
    _reward_utils = sm_reward_utils.get_instance()
    _reward_utils.fetch_wp_rewards(self)
    return True
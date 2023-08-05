from odoo import models, api
from odoo.addons.sm_rewards.models.models_sm_reward_utils import sm_reward_utils


class sm_cron(models.Model):
  _name = 'sm_rewards.reward_cron'

  @api.model
  def fetch_complete_rewards_from_wp(self):
    _reward_utils = sm_reward_utils.get_instance()
    _reward_utils.fetch_wp_rewards(self)
    _reward_utils.complete_rewards(self)

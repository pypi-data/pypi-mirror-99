# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.translate import _

class sm_member_related_coupon(models.Model):
  _name = 'sm_rewards.sm_member_related_coupon'

  name = fields.Char(string=_("Name"), required=True)
  related_member_id = fields.Many2one('res.partner', string=_("Related member"))
  wp_member_id = fields.Integer(string=_("wp Member ID"))

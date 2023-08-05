# -*- coding: utf-8 -*-
from odoo import fields, models, _

class ResConfigSettings(models.TransientModel):
  _inherit = 'res.config.settings'

  percentage_extra_minutes_cost = fields.Integer(
    related='company_id.percentage_extra_minutes_cost',
    string=_("percentage_extra_minutes_cost"))

  percentage_not_used = fields.Integer(
    related='company_id.percentage_not_used',
    string=_("percentage_not_used"))

  maxim_kms_per_hour = fields.Integer(
    related='company_id.maxim_kms_per_hour',
    string=_("Maxim kms per hour"))

  maxim_kms_per_day = fields.Integer(
    related='company_id.maxim_kms_per_day',
    string=_("Maxim kms per day"))


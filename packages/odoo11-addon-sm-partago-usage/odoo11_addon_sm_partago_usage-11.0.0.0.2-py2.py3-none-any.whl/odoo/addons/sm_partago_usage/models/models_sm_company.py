# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _

class sm_company(models.Model):
  _inherit = 'res.company'

  percentage_extra_minutes_cost = fields.Integer(_('Percentage of extra minutes cost'))
  percentage_not_used = fields.Integer(_('Percentage of extra minutes cost'))
  maxim_kms_per_hour = fields.Integer(_('Maxim kms per hour'))
  maxim_kms_per_day = fields.Integer(_('Maxim kms per day'))
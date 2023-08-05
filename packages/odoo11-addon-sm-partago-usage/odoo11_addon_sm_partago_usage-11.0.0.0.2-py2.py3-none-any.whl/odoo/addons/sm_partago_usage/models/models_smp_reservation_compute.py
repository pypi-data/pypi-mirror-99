# -*- coding: utf-8 -*-

import time
from datetime import datetime

from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.addons.sm_maintenance.models.models_sm_resources import sm_resources
from odoo.addons.sm_partago_invoicing.models.models_reservation_calculator import reservation_calculator
from odoo.tools.translate import _
from odoo.addons.sm_connect.models.models_sm_carsharing_db_utils import sm_carsharing_db_utils
from odoo.exceptions import ValidationError

class smp_reservation_compute(models.Model):
  _name = 'smp.sm_reservation_compute'

  name = fields.Char(string=_("Name"), required=True)
  name_nice = fields.Char(string=_("Name (Invoice line)"), compute="_get_compute_name_nice", store=False)
  member_id = fields.Many2one('res.partner', string=_("Member"))
  cs_user_type = fields.Char(string=_("cs user type"),compute="_get_cs_user_type", store=False)
  carconfig_id = fields.Many2one('smp.sm_car_config', string=_("Car (config)"))
  startTime = fields.Datetime(string=_("Start"))
  endTime = fields.Datetime(string=_("End"))
  effectiveStartTime = fields.Datetime(string=_("Effective Start"))
  effectiveEndTime = fields.Datetime(string=_("Effective End"))
  duration = fields.Float(string=_("Duration"))
  effectiveDuration = fields.Float(string=_("Effective Duration"))
  initial_fuel_level = fields.Float(string=_("Initial fuel level"))
  final_fuel_level = fields.Float(string=_("Final fuel level"))
  fuel_consume = fields.Float(string=_("Fuel consume"))
  used_mileage = fields.Float(string=_("Used mileage"))
  compute_invoiced = fields.Boolean(string=_("Compute invoiced"))
  compute_forgiven = fields.Boolean(string=_("Compute forgiven"))
  compute_cancelled = fields.Boolean(string=_("Compute cancelled"))
  compute_unused = fields.Boolean(_("Compute unused"))
  ignore_update = fields.Boolean(string=_("Ignore update"))
  usage_mins_invoiced = fields.Float(string=_("Used mins (Total)"))
  non_usage_mins_invoiced = fields.Float(string=_("Not used mins (Total)"))
  extra_usage_mins_invoiced = fields.Float(string=_("Extra used mins (Total)"))
  usage_mins_tariff = fields.Float(string=_("Used mins (Tariff)"))
  non_usage_mins_tariff = fields.Float(string=_("Not used mins (Tariff)"))
  extra_usage_mins_tariff = fields.Float(string=_("Extra used mins (Tariff)"))
  usage_mins_nontariff = fields.Float(string=_("Used mins (NONtariff)"))
  non_usage_mins_nontariff = fields.Float(string=_("Not used mins (NONtariff)"))
  extra_usage_mins_nontariff = fields.Float(string=_("Extra used mins (NONtariff)"))
  total_usage_mins_tariff = fields.Float(string=_("Total used mins (tariff-invoice)"))
  total_usage_days_tariff = fields.Float(string=_("Total used days (tariff-invoice)"))
  total_usage_mins_invoiced = fields.Float(string=_("Total used mins (NONtariff-invoice)"))
  total_usage_days_invoiced = fields.Float(string=_("Total used days (NONtariff-invoice)"))
  fuel_consume_invoiced = fields.Float(string=_("Fuel consume (invoice)"))
  used_mileage_invoiced = fields.Float(string=_("Used mileage (invoice)"))
  startTimechar = fields.Char(string=_("Start"), compute="_get_startTimechar", store=True)
  endTimechar = fields.Char(string=_("End"), compute="_get_endTimechar", store=False)
  effectiveStartTimechar = fields.Char(string=_("Effective Start"), compute="_get_effectiveStartTimechar",
    store=False)
  effectiveEndTimechar = fields.Char(string=_("Effective End"), compute="_get_effectiveEndTimechar",
    store=False)
  observations = fields.Text(string=_("Observations"))
  current_car = fields.Char(_("Associated car"))
  related_current_car = fields.Many2one('smp.sm_car', string=_("Associated car(Related)"),
    compute="get_related_associated_car")
  related_company = fields.Char(string=_("Company"))
  related_company_object = fields.Many2one('res.partner', string=_("Company"), compute="set_company_object")
  credits = fields.Float(_("Credits"))
  price = fields.Float(_("Price"))

  _order = "startTime desc"
  
  @api.constrains('name')
  def _check_name_unique(self):
    names_found = self.env['smp.sm_reservation_compute'].search([('id', '!=', self.id),('name', '=', self.name)])
    if names_found.exists(): 
      raise ValidationError(_("Name must be unique"))

  @api.depends('related_company')
  def set_company_object(self):
    for record in self:
      current_company_text = record.related_company
      if current_company_text:
        company_object = self.env['res.partner'].search([
          ('social_reason', '=', current_company_text)
        ])
        if company_object:
          record.related_company_object = company_object

  @api.model
  def reset_current_car_from_action(self):
    if self.env.context:
      if 'active_ids' in self.env.context:
        computes = self.env['smp.sm_reservation_compute'].browse(self.env.context['active_ids'])
        if computes.exists():
          for compute in computes:
            compute.reset_current_car()

  def reset_current_car(self):
    try:
      res_data = self.name.split('/', 1)
      db_utils = sm_carsharing_db_utils.get_instance()

      car = res_data[0]
      timestamp = res_data[1]

      endpoint_computed = "reservations/" + car
      rbp_query = db_utils.firebase_get(endpoint=endpoint_computed, key=timestamp)

      res_current_car = rbp_query.get("currentCar")

      if res_current_car is not None:
        self.current_car = res_current_car
      else:
        resource_car = rbp_query.get("resource")
        if resource_car is not None:
          self.current_car = resource_car
        else:
          car = get_reservation_dbcar_obj()
          if car:
            self.current_car = car.name
          else:
            self.current_car = -1
    except:
      print("error " + str(self.id))

  def get_reservation_dbcar_obj(self):
    if not self.related_current_car:
      rel_carconfig = self.carconfig_id
      if rel_carconfig:
        return rel_carconfig.rel_car_id
      return False
    else:
      return self.related_current_car

  def get_cs_carconfig_obj(self):
    if self.carconfig_id.id != False:
      rel_cs_carconfig = self.env['sm_carsharing_structure.cs_carconfig'].search([('db_carconfig_id','=',self.carconfig_id.id)])
      if rel_cs_carconfig.exists():
        return rel_cs_carconfig[0]
    return False

  def get_analytic_account(self):
    company = self.env.user.company_id
    analytic_account = company.notfound_car_analytic_account_id

    # find a better analytic account for line
    cs_carconfig = self.get_cs_carconfig_obj()
    if cs_carconfig:
      analytic_account = cs_carconfig.analytic_account_id

    return analytic_account

  def get_teletac_analytic_account(self):
    company = self.env.user.company_id
    analytic_account = company.notfound_teletac_analytic_account_id

    # find a better analytic account for line
    # find a better analytic account for line
    cs_carconfig = self.get_cs_carconfig_obj()
    if cs_carconfig:
      analytic_account = cs_carconfig.teletac_analytic_account_id

    return analytic_account

  @api.depends('current_car')
  def get_related_associated_car(self):
    related_current_car = None
    for record in self:
      current_car = record.current_car
      if current_car != -1:
        related_current_car = self.env['smp.sm_car'].search([
          ('name', '=', current_car)
        ])
      if related_current_car is not None:
        record.related_current_car = related_current_car

  @api.constrains('effectiveStartTime', 'effectiveEndTime', 'startTime', 'endTime')
  def update(self):
    for record in self:
      self.update_duration(record)

  def update_duration(self, record):
    fmt = '%Y-%m-%d %H:%M:%S'

    effective_end = datetime.strptime(record.effectiveEndTime, fmt)
    effective_start = datetime.strptime(record.effectiveStartTime, fmt)

    effective_end_ts = time.mktime(effective_end.timetuple())
    effective_start_ts = time.mktime(effective_start.timetuple())

    effective_duration = int(effective_end_ts - effective_start_ts) / 60

    end = datetime.strptime(record.endTime, fmt)
    start = datetime.strptime(record.startTime, fmt)

    end_ts = time.mktime(end.timetuple())
    start_ts = time.mktime(start.timetuple())

    duration = int(end_ts - start_ts) / 60

    self.write_invoiced_parameters(record)

    record.write({
      'duration': duration,
      'effectiveDuration': effective_duration
    })

  @api.depends('member_id')
  def _get_cs_user_type(self):
    for record in self:
      record.cs_user_type = str(record.member_id.cs_user_type)

  @api.depends('startTime')
  def _get_startTimechar(self):
    for record in self:
      record.startTimechar = str(record.startTime)

  @api.depends('endTime')
  def _get_endTimechar(self):
    for record in self:
      record.endTimechar = str(record.endTime)

  @api.depends('effectiveStartTime')
  def _get_effectiveStartTimechar(self):
    for record in self:
      record.effectiveStartTimechar = str(record.effectiveStartTime)

  @api.depends('effectiveEndTime')
  def _get_effectiveEndTimechar(self):
    for record in self:
      record.effectiveEndTimechar = str(record.effectiveEndTime)

  @api.depends('startTime', 'effectiveStartTime', 'carconfig_id')
  def _get_compute_name_nice(self):
    # calculate invoice line name
    for record in self:
      if record.effectiveStartTime < record.startTime:
        starttimecalc = record.effectiveStartTime
      else:
        starttimecalc = record.startTime
      start_time = datetime.strptime(starttimecalc, "%Y-%m-%d %H:%M:%S")
      start_time_str = start_time.strftime("%H:%M-%d/%m/%y")
      record.name_nice = record.carconfig_id.carconfig_name + \
        '-[' + start_time_str + ']'

  @api.multi
  def mark_as_forgiven(self):
    if self.env.context:
      if 'active_ids' in self.env.context:
        computes = self.env['smp.sm_reservation_compute'].browse(self.env.context['active_ids'])
        if computes.exists():
          for compute in computes:
            compute.write({'compute_forgiven': True})

    return sm_resources.getInstance().get_successful_action_message(self, _('Mark as forgiven done successfully'),
      self._name)

  @api.multi
  def mark_as_toinvoice(self):
    if self.env.context:
      if 'active_ids' in self.env.context:
        computes = self.env['smp.sm_reservation_compute'].browse(self.env.context['active_ids'])
        if computes.exists():
          for compute in computes:
            compute.write({
              'compute_forgiven': False,
              'compute_invoiced': False
            })

    return sm_resources.getInstance().get_successful_action_message(self, _('Mark as toInvoice done successfully'),
      self._name)

  @api.multi
  def calculate_values(self):
    if self.env.context:
      if 'active_ids' in self.env.context:
        computes = self.env['smp.sm_reservation_compute'].browse(self.env.context['active_ids'])
        if computes.exists():
          for compute in computes:
            self.write_invoiced_parameters(compute)

    return sm_resources.getInstance().get_successful_action_message(self, _('Calculate value done successfully'),
      self._name)

  def write_invoiced_parameters(self, compute):
    update_values = reservation_calculator.get_general_values(compute, 'object')
    compute.write({
      'usage_mins_invoiced': update_values['usage_mins'],
      'non_usage_mins_invoiced': update_values['non_usage_mins'],
      'extra_usage_mins_invoiced': update_values['extra_usage_mins']
    })

  @api.model
  def compute_report_invoice_vals(self, tariff):
    effectiveStartTime = datetime.strptime(self.effectiveStartTime, "%Y-%m-%d %H:%M:%S")
    startTime = datetime.strptime(self.startTime, "%Y-%m-%d %H:%M:%S")

    effectiveEndTime = datetime.strptime(self.effectiveEndTime, "%Y-%m-%d %H:%M:%S")
    endTime = datetime.strptime(self.endTime, "%Y-%m-%d %H:%M:%S")

    res_params = {
      'applied_tariff_id': tariff['tariff_id']
    }

    # Calculate real start for computation
    if effectiveStartTime < startTime:
      real_start = effectiveStartTime
    else:
      real_start = startTime

    # Calculate real end for computation
    if effectiveEndTime < endTime:
      real_end = effectiveEndTime
    else:
      real_end = endTime

    decoupled_mins = self.decouple_mins_between_tariff_and_non(self.usage_mins_invoiced, tariff['tariff_aval'],
      real_start, real_end)
    res_params['usage_mins_tariff'] = decoupled_mins['tariff']
    res_params['usage_mins_nontariff'] = decoupled_mins['nontariff']

    # not used mins
    if endTime >= effectiveEndTime:
      decoupled_mins = self.decouple_mins_between_tariff_and_non(self.non_usage_mins_invoiced,
        tariff['tariff_aval'], effectiveEndTime, endTime)
      res_params['non_usage_mins_tariff'] = decoupled_mins['tariff']
      res_params['non_usage_mins_nontariff'] = decoupled_mins['nontariff']
      res_params['extra_usage_mins_tariff'] = 0
      res_params['extra_usage_mins_nontariff'] = 0

    else:
      decoupled_mins = self.decouple_mins_between_tariff_and_non(self.extra_usage_mins_invoiced,
        tariff['tariff_aval'], endTime, effectiveEndTime)
      res_params['extra_usage_mins_tariff'] = decoupled_mins['tariff']
      res_params['extra_usage_mins_nontariff'] = decoupled_mins['nontariff']
      res_params['non_usage_mins_tariff'] = 0
      res_params['non_usage_mins_nontariff'] = 0

    # Calculate days and minutes
    # fallback values
    company = self.env.user.company_id
    percentage_not_used = 1
    percentage_extra = 1
    kms_included_day = 200
    kms_included_hour = 30

    if company:
      percentage_not_used = company.percentage_not_used / 100
      percentage_extra = company.percentage_extra_minutes_cost / 100
      kms_included_day = company.maxim_kms_per_day
      kms_included_hour = company.maxim_kms_per_hour

    total_mins_reservation_tariff = res_params['usage_mins_tariff'] + percentage_not_used * res_params[
      'non_usage_mins_tariff'] + percentage_extra * res_params['extra_usage_mins_tariff']
    rvals = reservation_calculator.decouple_reservation_days_and_mins(total_mins_reservation_tariff)
    res_params['invoice_days_tariff'] = rvals['days']
    res_params['invoice_mins_tariff'] = rvals['mins']

    total_mins_reservation_nontariff = res_params['usage_mins_nontariff'] + percentage_not_used * res_params[
      'non_usage_mins_nontariff'] + percentage_extra * res_params['extra_usage_mins_nontariff']
    rvals = reservation_calculator.decouple_reservation_days_and_mins(total_mins_reservation_nontariff)
    res_params['invoice_days_nontariff'] = rvals['days']
    res_params['invoice_mins_nontariff'] = rvals['mins']

    # mileage_consume
    total_invoice_days = res_params['invoice_days_tariff'] + res_params['invoice_days_nontariff']
    total_invoice_mins = res_params['invoice_mins_tariff'] + res_params['invoice_mins_nontariff']

    used_mileage_invoiced = self.used_mileage - (kms_included_day * total_invoice_days) - (
      kms_included_hour * reservation_calculator.get_hours_from_minutes(total_invoice_mins))
    if used_mileage_invoiced < 0:
      used_mileage_invoiced = 0
    res_params['used_mileage_invoiced'] = used_mileage_invoiced

    self.update_reservation_compute(res_params)
    self.apply_min_reservation_time_restriction()

  def compute_invoice_report_tariff_time_quantities(self, tariff_model):
    prices = tariff_model.get_prices(self.carconfig_id)
    tariff_day_price = prices['day_price'].product_tmpl_id.list_price
    tariff_min_price = prices['min_price'].product_tmpl_id.list_price
    return self.total_usage_mins_tariff * tariff_min_price + self.total_usage_days_tariff * tariff_day_price

  def compute_invoice_report_nontariff_time_quantities(self, tariff_model):
    prices = tariff_model.get_prices(self.carconfig_id)
    tariff_day_price = prices['day_price'].product_tmpl_id.list_price
    tariff_min_price = prices['min_price'].product_tmpl_id.list_price
    return self.total_usage_mins_invoiced * tariff_min_price + self.total_usage_days_invoiced * tariff_day_price

  def compute_invoice_report_km_quantities(self, tariff_model):
    prices = tariff_model.get_prices(self.carconfig_id)
    tariff_km_price = prices['kms_price'].product_tmpl_id.list_price
    return self.used_mileage_invoiced * tariff_km_price

  def update_reservation_compute(self, res_params):
    udata = {
      'used_mileage_invoiced': res_params['used_mileage_invoiced'],
      'usage_mins_tariff': res_params['usage_mins_tariff'],
      'non_usage_mins_tariff': res_params['non_usage_mins_tariff'],
      'extra_usage_mins_tariff': res_params['extra_usage_mins_tariff'],
      'usage_mins_nontariff': res_params['usage_mins_nontariff'],
      'non_usage_mins_nontariff': res_params['non_usage_mins_nontariff'],
      'extra_usage_mins_nontariff': res_params['extra_usage_mins_nontariff'],
      'total_usage_mins_invoiced': res_params['invoice_mins_nontariff'],
      'total_usage_days_invoiced': res_params['invoice_days_nontariff'],
      'total_usage_mins_tariff': res_params['invoice_mins_tariff'],
      'total_usage_days_tariff': res_params['invoice_days_tariff'],
      'applied_tariff_id': res_params['applied_tariff_id']
    }

    self.write(udata)

  def apply_min_reservation_time_restriction(self):
    min_reservation_time = 60
    if self.total_usage_mins_tariff == 0 and self.total_usage_days_tariff == 0:
      if self.total_usage_days_invoiced == 0 and self.total_usage_mins_invoiced < min_reservation_time:
        self.write({'total_usage_mins_invoiced':min_reservation_time})


  def check_mins_in_tariff(self, avals_txt, start_datetime, end_datetime):
    mins = 0

    avals = self.prepare_tariff_avals(avals_txt)

    start_initial = {'day': start_datetime.weekday(
    ), 'hour': start_datetime.strftime("%H:%M")}
    end_initial = {'day': end_datetime.weekday(
    ), 'hour': end_datetime.strftime("%H:%M")}

    num_weeks = 0
    if start_datetime.isocalendar()[1] != end_datetime.isocalendar()[1]:
      num_weeks = end_datetime.isocalendar(
      )[1] - start_datetime.isocalendar()[1]

    # TODO: control different years!!!!
    if num_weeks > 0:
      start = start_initial
      start_week = {
        'day': 0,
        'hour': '00:00'
      }
      end_week = {
        'day': 6,
        'hour': '23:59'
      }
      i = 1
      mins = mins + self.check_mins_in_tariff_in_week(avals, start, end_week)

      while i < num_weeks:
        mins = mins + self.check_mins_in_tariff_in_week(avals, start_week, end_week)
        i = i + 1

      mins = mins + self.check_mins_in_tariff_in_week(avals, start_week, end_initial)
    else:
      mins = self.check_mins_in_tariff_in_week(
        avals, start_initial, end_initial)

    return mins

  def check_mins_in_tariff_in_week(self, avals, start, end):
    mins = 0

    for aval_key in avals:
      interval_start = {
        'day': avals[aval_key]['start_day'],
        'hour': avals[aval_key]['start_hour']
      }
      interval_end = {
        'day': avals[aval_key]['end_day'],
        'hour': avals[aval_key]['end_hour']
      }
      if self.week_time_compare(start, '>', interval_start) and self.week_time_compare(start, '<',
        interval_end) and self.week_time_compare(end, '>', interval_start) and \
        self.week_time_compare(end, '<', interval_end):
        mins = mins + self.week_time_diff(start, end)
      else:
        if self.week_time_compare(start, '>', interval_start) and self.week_time_compare(start, '<',
          interval_end):
          mins = mins + self.week_time_diff(start, interval_end)
        else:
          if self.week_time_compare(end, '>', interval_start) and self.week_time_compare(end, '<',
            interval_end):
            mins = mins + self.week_time_diff(interval_start, end)
          else:
            if self.week_time_compare(start, '<', interval_start) and self.week_time_compare(end, '>',
              interval_end):
              mins = mins + self.week_time_diff(interval_start, interval_end)

    return mins

  def decouple_mins_between_tariff_and_non(self, total_mins, tariff_avals, start_datetime, end_datetime):
    decoupled = {}
    if tariff_avals:
      tariff_avals_mins = self.check_mins_in_tariff(tariff_avals, start_datetime, end_datetime)
      decoupled['tariff'] = tariff_avals_mins
      decoupled['nontariff'] = total_mins - tariff_avals_mins
    else:
      decoupled['tariff'] = 0
      decoupled['nontariff'] = total_mins
    return decoupled

  def get_weekday(self, day_str):
    if day_str == 'Mon':
      return 0
    if day_str == 'Tue':
      return 1
    if day_str == 'Wed':
      return 2
    if day_str == 'Thu':
      return 3
    if day_str == 'Fri':
      return 4
    if day_str == 'Sat':
      return 5
    if day_str == 'Sun':
      return 6

  def prepare_tariff_avals(self, avals_txt):
    aval_dict = {}
    i = 0
    days = avals_txt.split('+')
    for day in days:
      day_range = day.split('-')
      start = day_range[0].split(' ')
      end = day_range[1].split(' ')
      aval_dict[i] = {
        'start_day': self.get_weekday(start[0]),
        'start_hour': start[1],
        'end_day': self.get_weekday(end[0]),
        'end_hour': end[1]
      }
      i = i + 1
    return aval_dict

  def week_time_compare(self, time1, case, time2):
    if case == '<':
      if time1['day'] <= time2['day']:
        if time1['day'] == time2['day']:
          if datetime.strptime(time1['hour'], '%H:%M') <= datetime.strptime(time2['hour'], '%H:%M'):
            return True
        else:
          return True
    if case == '>':
      if time1['day'] >= time2['day']:
        if time1['day'] == time2['day']:
          if datetime.strptime(time1['hour'], '%H:%M') >= datetime.strptime(time2['hour'], '%H:%M'):
            return True
        else:
          return True

    return False

  def week_time_diff(self, start, end):
    compute = True
    mins = 0
    i = start['day']
    if i <= end['day']:
      while compute:
        if i != end['day']:
          mins = mins + 24 * 60
          i = i + 1
        else:
          rest = (datetime.strptime(
            end['hour'], '%H:%M') - datetime.strptime(start['hour'], '%H:%M')).total_seconds() / 60.00
          mins = mins + rest
          compute = False
    return mins
    
  def autoforgive(self):
    if self.env.context:
      if 'active_ids' in self.env.context:
        selected_reservations = self.env['smp.sm_reservation_compute'].browse(self.env.context['active_ids'])
        if selected_reservations.exists():
          for reserv in selected_reservations:
            if reserv.cs_user_type in ['promo','maintenance']:
              reserv.write({'compute_forgiven':True})
            
  @api.model
  def get_wizard_view(self):
    view_ref = self.env['ir.ui.view'].sudo().search(
      [('name', '=', 'sm_partago_invoicing.sm_batch_reservation_compute.wizard')])
    return view_ref.id

  def get_edit_wizard_view(self):
    view_ref = self.env['ir.ui.view'].sudo().search(
      [('name', '=', 'sm_partago_usage.edit_reservation_compute_wizard.form')])
    return view_ref.id

  @api.multi
  def create_edit_reservation_compute_wizard(self):
    if self.env.context:
      return {
        'type': 'ir.actions.act_window',
        'name': "Edit reservation compute",
        'res_model': 'smp.sm_edit_reservation_compute_wizard',
        'view_type': 'form',
        'view_mode': 'form',
        'view_id': self.get_edit_wizard_view(),
        'target': 'new',
        'context': self.env.context
      }

  @api.model
  def test(self):
    view_id = self.env['sm_partago_invoicing.sm_batch_reservation_compute.wizard'].create({})

    return {
      'type': 'ir.actions.act_window',
      'name': 'Create batch compute',
      'res_model': 'sm_partago_invoicing.sm_batch_reservation_compute.wizard',
      'view_type': 'form',
      'view_mode': 'form',
      'res_id': view_id.id,
      'view_id': self.get_wizard_view(),
      'target': 'new',
      'context': self.env.context,
    }

# -*- coding: utf-8 -*-
import os
import re
import json
import time
import unicodedata
from datetime import datetime

from schwifty import IBAN

from odoo import models, fields, api
from odoo.tools.translate import _

from odoo.addons.sm_maintenance.models.models_sm_utils import sm_utils
from odoo.addons.sm_maintenance.models.models_sm_resources import sm_resources



class sm_member(models.Model):
  # TODO: check why this is needed
  ADDRESS_FIELDS = ('street', 'street2', 'zip', 'city', 'state_id')
  
  _inherit = 'res.partner'
  _name = 'res.partner'

  # TODO: change this to custom odoo notification system
  _resources = sm_resources.getInstance()
  
  # TODO: Fields to be moved to EMC
  member_nr = fields.Integer(string=_("Member number"))
  gender = fields.Selection([
    ('man', 'Man'),
    ('woman', 'Woman')],
    _('Gender'))


  # TODO: Fields going to OCA https://github.com/OCA/partner-contact/tree/12.0/partner_firstname
  firstname = fields.Char(string=_("Name"))
  surname = fields.Char(string=_("Last name"),compute='_get_surname',store=True)

  # TODO: Fields to be deleted
  first_surname = fields.Char(string=_("First surname"))
  second_surname = fields.Char(string=_("Second surname"))

  # TODO: Move this to Odoo core to vat
  cif = fields.Char(string=_("CIF"))
  dni = fields.Char(string=_("DNI/NIF"))

  # TODO: move this to base_vat and vatnumber
  id_document_type = fields.Selection([
    ('dni', 'DNI'),
    ('nie', 'NIE'),
  ], string=_("ID Document"), compute="_set_id_document_type", store=True)

  # TODO: move to name and "comercial_name"
  social_reason = fields.Char(string=_("Business name"))

  # TODO: make this core Odoo
  state = fields.Char(string=_("Province"))
  
  # TODO: move this field to "mobile" field
  phone_2 = fields.Char(string=_("Phone 2"))

  # TODO: to be deleted
  bank_account_type = fields.Selection([
    ('account_nr', 'Corrent'),
    ('iban', 'IBAN')],
    _('Account type'))
  # TODO: delete but checking that no data get lost (i.e we have an IBAN defined)
  bank_account_nr_1 = fields.Char(string=_("Corrent1"))
  bank_account_nr_2 = fields.Char(string=_("Corrent2"))
  bank_account_nr_3 = fields.Char(string=_("Corrent3"))
  bank_account_nr_4 = fields.Char(string=_("Corrent4"))
  # This stays only on wordpress and we send IBAN1+...+IBAN6 from wordpress to subscription request
  iban_1 = fields.Char(string=_("IBAN 1"))
  iban_2 = fields.Char(string=_("IBAN 2"))
  iban_3 = fields.Char(string=_("IBAN 3"))
  iban_4 = fields.Char(string=_("IBAN 4"))
  iban_5 = fields.Char(string=_("IBAN 5"))
  iban_6 = fields.Char(string=_("IBAN 6"))
  # TODO: make some test on production database, make sure we don't lose data
  # TODO: handle duplicated IBANs without bank accounts
  # **TODO: handle bank _account general strategy
  invoicing_iban = fields.Char(string=_("Invoicing IBAN"))

  # TODO: To be deleted
  bank_correct = fields.Boolean(string=_("Correct bank account"))
  bank_correct_validation = fields.Boolean(string=_("Correct bank account (validation)"))

  # TODO: move to EMC
  membership_success = fields.Boolean(string=_("Completed cooperative registration"))
  cooperative_member = fields.Boolean(string=_("Cooperative Member"))

  # TODO: core "name" must be used
  member_name = fields.Char(string=_("Member name"), compute="_get_member_name", store=False)

  # rename to something generic, move to EMC subscription request. It shows from where subscription request has been created
  wp_member_id = fields.Integer(string=_("wp Member ID"))

  # TODO: move to vertical_carsharing. member_nr will change field name
  _order = "member_nr desc"

  @api.depends('first_surname', 'second_surname')
  def _get_surname(self):
    for record in self:
      surname = ''
      if record.first_surname:
        surname += record.first_surname
      if record.second_surname:
        surname += ' ' + record.second_surname
      record.surname = surname

  @api.depends('dni')
  def _set_id_document_type(self):
    for record in self:
      if record.company_type == 'person':
        dni_nie = record.dni
        if dni_nie:
          dni_pattern = re.compile("^[0-9]{8}[a-zA-Z]$")
          nie_patter = re.compile("^[a-zA-Z][0-9]{7}[a-zA-Z]$")
          if dni_pattern.match(dni_nie):
            record.id_document_type = "dni"
          elif nie_patter.match(dni_nie):
            record.id_document_type = "nie"

  @api.depends('firstname', 'first_surname', 'second_surname', 'social_reason', 'company_type')
  def _get_member_name(self):
    for record in self:
      full_name = ''
      if record.company_type == 'person':
        if record.firstname:
          full_name += record.firstname
        if record.surname:
          full_name += ' ' + record.surname
      else:
        if record.social_reason:
          full_name = record.social_reason
      record.member_name = full_name

  # TODO: Delete this!
  def get_member_erp_name(self):
    erp_name = ''
    if self.company_type == 'person':
      if self.surname:
        erp_name += self.surname
      if self.firstname:
        erp_name += ', ' + self.firstname
    else:
      if self.social_reason:
        erp_name = self.social_reason
    return erp_name
  # TODO: Delete this!
  @api.multi
  @api.onchange('firstname', 'first_surname', 'second_surname','social_reason')
  @api.constrains('firstname', 'first_surname', 'second_surname','social_reason')
  def setup_sm_member_name(self):
      self.name = self.get_member_erp_name()

  # TODO: EMC SR workflow
  @api.model
  def mark_as_completed(self):
    if self.env.context:
      if 'active_ids' in self.env.context:
        members = self.env['res.partner'].browse(
          self.env.context['active_ids'])
        if members.exists():
          for member in members:
            member.sudo().write({'membership_success': True})
    return self._resources.get_successful_action_message(self,
      _('Mark as completed done successfully'), self._name)

  # TODO: EMC SR workflow
  @api.model
  def activate_member_from_action(self):
    if self.env.context:
      if 'active_ids' in self.env.context:
        members = self.env['res.partner'].browse(self.env.context['active_ids'])
        if members.exists():
          for member in members:
            member.activate_member()
    return self._resources.get_successful_action_message(self,
      _('Activate member done successfully'), self._name)

  # TODO: EMC SR workflow
  def activate_member(self):
    self.validate_bank_account()
    self.create_system_bank_account() # mirar si el IBAN es valid (invoice IBAN definit) i establir res.partner.bank
    self.mark_as_correct_bank_account()
    if self.member_nr > 0:
      self.mark_as_cooperative()
    self.reformat_data()

  # TODO: EMC SR workflow
  @api.model
  def compute_invoice_fields_from_action(self):
    if self.env.context:
      if 'active_ids' in self.env.context:
        members = self.env['res.partner'].browse(self.env.context['active_ids'])
        if members.exists():
          for member in members:
            member.validate_bank_account()

  # TODO: EMC SR workflow
  @api.multi
  def mark_as_cooperative_from_action(self):
    if self.env.context:
      if 'active_ids' in self.env.context:
        members = self.env['res.partner'].browse(self.env.context['active_ids'])
        if members.exists():
          for member in members:
            member.mark_as_cooperative()
    return self._resources.get_successful_action_message(self,
      _('Mark as cooperative done successfully'), self._name)

  # TODO: EMC SR workflow
  def mark_as_cooperative(self):
    self.sudo().write({'cooperative_member': True})

  # **TODO: EMC SR workflow
  @api.model
  def mark_as_correct_bank_account_from_action(self):
    if self.env.context:
      if 'active_ids' in self.env.context:
        members = self.env['res.partner'].browse(self.env.context['active_ids'])
        if members.exists():
          for member in members:
            member.mark_as_correct_bank_account()

    return self._resources.get_successful_action_message(self,
      _('Mark as correct bank account done successfully'), self._name)

  # **TODO: EMC SR workflow
  def mark_as_correct_bank_account(self):
    self.bank_correct = True

  # **TODO: EMC SR workflow
  @api.model
  def validate_bank_account_from_action(self):
    if self.env.context:
      if 'active_ids' in self.env.context:
        members = self.env['res.partner'].browse(self.env.context['active_ids'])
        if members.exists():
          for member in members:
            member.validate_bank_account()

    return self._resources.get_successful_action_message(self,
      _('Validate bank account done successfully'), self._name)

  # **TODO: EMC SR workflow
  def validate_bank_account(self):
    correct = False
    iban = None

    if self.iban_1:
      self.iban_1 = self.iban_1.upper().strip()

    if self.bank_account_type == 'account_nr':
      if self.bank_account_nr_1 and self.bank_account_nr_2 and self.bank_account_nr_3 \
        and self.bank_account_nr_4:
        bank_nr = False
        try:
          bank_nr = IBAN.generate('ES', bank_code=str(self.bank_account_nr_1).upper().strip() 
          + str(self.bank_account_nr_2).upper().strip() ,
          account_code=str(self.bank_account_nr_3).upper().strip()
          + str(self.bank_account_nr_4).upper().strip())
        except ValueError:
          correct = False
        if bank_nr:
          iban = False
          try:
            iban = IBAN(str(bank_nr))
          except ValueError:
            correct = False
          if iban:
            iban_str = str(iban)
            if sm_utils.generate_iban_check_digits(iban) == iban_str[2:4] and sm_utils.valid_iban(iban):
              correct = True

    if self.bank_account_type == 'iban':
      if self.iban_1 and self.iban_2 and self.iban_3 and self.iban_4 and self.iban_5 \
        and self.iban_6:
        iban = False
        try:
          iban = IBAN(self.get_bank_nr())
        except ValueError:
          correct = False
        if iban:
          iban_str = str(iban)
          if sm_utils.generate_iban_check_digits(iban) == iban_str[2:4] and sm_utils.valid_iban(iban):
            correct = True
    if correct:
      self.sudo().write({'bank_correct_validation': True})
      if iban is not None:
        self.write({
          'invoicing_iban': str(iban).strip()
        })
    else:
      self.sudo().write({'bank_correct_validation': False})
      return False

    return True

  # **TODO: EMC SR workflow
  @api.model
  def migrate_bank_account_action(self):
    if self.env.context:
      if 'active_ids' in self.env.context:
        members = self.env['res.partner'].browse(self.env.context['active_ids'])
        if members.exists():
          for member in members:
            member.create_system_bank_account()

  # **TODO: EMC SR workflow
  def migrate_bank_account(self):
    if self.invoicing_iban:
      existing_bank_accounts = self.env['res.partner.bank'].search(
        [('acc_number', '=', self.invoicing_iban)]) 
      if existing_bank_accounts.exists():
        existing_bank_account = existing_bank_accounts[0] 
        if existing_bank_account.partner_id.id != self.id:
          # query = [
          #   ('error_message', '=', "L'IBAN és duplicat per l'usuari [ "+str(existing_bank_account.partner_id.id) + " ]"),
          #   ('related_member_id', '=', self.id),
          # ]
          # creation_data = {
          #   'error_message': "L'IBAN és duplicat per l'usuari [ "+str(existing_bank_account.partner_id.id) + " ]",
          #   'related_member_id': self.id,
          # }
          # sm_utils.get_create_existing_model(self.env['sm.sm_error'], query, creation_data)
          return False
        else:
          #tot OK
          return True
      query = [
        ('acc_number', '=', self.invoicing_iban),
        ('partner_id', '=', self.id),
      ]
      creation_data = {
        "acc_number": self.invoicing_iban,
        "partner_id": self.id
      }
      sm_utils.get_create_existing_model(self.env['res.partner.bank'], query, creation_data)
      #TODO: si hem arribat fins aqui (que vol dir que el nou bank account no existeix) mirarem si la persona (self) te altres bacnk accounts i cancelarem els mandats relacionats en aquest bank accout

  # **TODO: EMC SR workflow
  def create_system_bank_account(self):
    if self.validate_bank_account():
      self.migrate_bank_account()
    self.create_banking_mandate()
    return True

  def create_banking_mandate(self):
    existing_bank_acc = self.env['res.partner.bank'].search([('partner_id','=',self.id)])
    if existing_bank_acc.exists():
      for bank_acc in existing_bank_acc:
        query = [
          ('partner_bank_id', '=', bank_acc.id),
          ('partner_id', '=', self.id),
        ]
        creation_data = {
          'format':'sepa',
          'type': 'recurrent',
          'partner_bank_id': bank_acc.id,
          'partner_id': self.id,
          'signature_date': datetime.now().isoformat(),
          'state': 'valid',
          'recurrent_sequence_type': 'recurring',
          'scheme': 'CORE'
        }
        obj = sm_utils.get_create_existing_model(self.env['account.banking.mandate'], query, creation_data)
    
  # **TODO: EMC SR workflow
  def get_bank_nr(self):
    if self.bank_account_type == 'account_nr':
      iban = IBAN.generate('ES', bank_code=str(self.bank_account_nr_1).upper().strip()
        + str(self.bank_account_nr_2).upper().strip() ,
        account_code=str(self.bank_account_nr_3).upper().strip()
        + str(self.bank_account_nr_4).upper().strip())
      
      return str(iban)
    else:
      striped_iban = str(self.iban_1).upper().strip() + str(self.iban_2).upper().strip() + str(self.iban_3).upper().strip() + str(self.iban_4).upper().strip() + str(self.iban_5).upper().strip() + str(self.iban_6).upper().strip()
      return striped_iban

  # TODO: delete (used only on batch_payment that won't be migrated)
  def get_sepa_name(self):
    sepa_name = ''.join(
      c for c in unicodedata.normalize('NFD',
      str(self.member_name)) if unicodedata.category(c) != 'Mn')
    return sepa_name

  # TODO: delete (wordpress must send correct data to SR, second cleanup on odoo)
  def reformat_data(self):
    u_data = {}
    if self.dni:
      u_data['dni'] = str(self.dni).replace("-", "").replace(" ", "").upper()
    if self.cif:
      u_data['cif'] = str(self.cif).replace("-", "").replace(" ", "").upper()
    if bool(u_data):
      self.write(u_data)

  # TODO: delete
  @api.model
  def sanitize_reporting_db_action(self):
    if self.env.context:
      if 'active_ids' in self.env.context:
        members = self.env['res.partner'].browse(self.env.context['active_ids'])
        if members.exists():
          for member in members:
            if member.maintenance_related_member:
              member.write({
                'reporting_related_member_id': member.maintenance_related_member.id
              })
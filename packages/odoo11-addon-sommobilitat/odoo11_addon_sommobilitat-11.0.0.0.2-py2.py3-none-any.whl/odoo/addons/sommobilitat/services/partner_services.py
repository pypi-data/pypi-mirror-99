# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.component.core import Component
from odoo.addons.sm_rest_api.models.models import validate_request

from odoo.addons.base_rest.components.service import to_int, to_bool
from odoo.http import Response


class PartnerService(Component):
  _inherit = 'base.rest.service'
  _name = 'partner.service'
  _usage = 'partner'
  _collection = 'partner.rest.public.services'
  _description = """
    Partner Services
    Access to the partner services is only allowed to authenticated users.
    If you are not authenticated go to <a href='/web/login'>Login</a>
  """

  def test(self, _id=None, **params):
    partners = self.env['res.partner'].sudo().search([('id', '=', _id)])
    return {
      'message': 'hello'
    }

  @validate_request
  def update_contact_info(self, _id=None, **params):
    partner = self.get_res_partner_by_uid(uid=params['uid'])
    partner.sudo().write({
      'phone': params['phone1'],
      'phone_2': params['phone2'],
      'email': params['email']
    })
    return Response("Actualitzat correctament", status=200)

  @validate_request
  def update_payment_info(self, _id=None, **params):
    partner = self.get_res_partner_by_uid(uid=params['uid'])
    partner.sudo().write({
      'iban_1': params['iban1'],
      'iban_2': params['iban2'],
      'iban_3': params['iban3'],
      'iban_4': params['iban4'],
      'iban_5': params['iban5'],
      'iban_6': params['iban6'],
      'invoicing_email': params['invoice_email']
    })
    return Response("Actualitzat correctament", status=200)

  @validate_request
  def update_address_info(self, _id=None, **params):
    partner = self.get_res_partner_by_uid(uid=params['uid'])
    partner.sudo().write({
      'street': params['street'],
      'zip': params['zip'],
      'computed_city': params['city'],
      'computed_state': params['province'],
    })
    return Response("Actualitzat correctament", status=200)

  @validate_request
  def update_general_info(self, _id=None, **params):
    partner = self.get_res_partner_by_uid(uid=params['uid'])
    partner.sudo().write({
      'firstname': params['name'],
      'first_surname': params['first_surname'],
      'second_surname': params['second_surname'],
      'birthday': params['birthday'],
      'dni': params['dni'],
    })
    return Response("Actualitzat correctament", status=200)

  def update_firebase_uid(self, _id=None, **params):
    partner = self.get_res_partner_by_member_nr(member_nr=params['member_nr'])
    partner.sudo().write({
      'firebase_uid': params['uid']
    })
    return {
      'message': 'Success'
    }

  def get_num_member(self, _id=None, **params):
    num_partners = self.env['res.partner'].sudo().search_count([('member_nr', '>', '0')])
    return {'num_socis': num_partners}

  def update(self, _id, **params):
    partner = self._get(_id)
    partner.write(self._prepare_params(params))
    return self._to_json(partner)

  def get_member_info(self, _id=None, **params):
    partner = self.get_res_partner_by_uid(uid=params['uid'])
    return self._to_json(self._get(partner.id))

  def search(self, name):
    """
    Searh partner by name
    """
    partners = self.env['res.partner'].name_search(name)
    partners = self.env['res.partner'].browse([i[0] for i in partners])
    rows = []
    res = {
      'count': len(partners),
      'rows': rows
    }
    for partner in partners:
      rows.append(self._to_json(partner))
    return res

  # pylint:disable=method-required-super
  def create(self, **params):
    """
    Create a new partner
    """
    last_member_nr_id = self.env['res.partner'].sudo().search([
      ("cooperative_member", "=", True)
    ], order="member_nr desc", limit=1).member_nr

    params['member_nr'] = last_member_nr_id + 1

    register_carsharing = params['register_carsharing']
    params['register_carsharing'] = self.cast_to_bool(register_carsharing)

    membership_success = params['membership_success']
    params['membership_success'] = self.cast_to_bool(membership_success)

    cooperative_member = params['cooperative_member']
    params['cooperative_member'] = self.cast_to_bool(cooperative_member)

    partner = self.env['res.partner'].sudo().create(
      self._prepare_params(params))
    return self._to_json(partner)

  def cast_to_bool(self, param):
    if param in ['true', '1', 't', 'y', 'yes', 'True']:
      return True
    return False

  def _get(self, _id):
    return self.env['res.partner'].sudo().search([('id', '=', _id)])

  def _prepare_params(self, params):
    for key in ['country', 'state']:
      if key in params:
        val = params.pop(key)
        if val.get('id'):
          params["%s_id" % key] = val['id']
    return params

  def get_res_partner_by_uid(self, uid):
    return self.env['res.partner'].sudo().search([('firebase_uid', '=', uid)])

  def get_res_partner_by_member_nr(self, member_nr):
    return self.env['res.partner'].sudo().search([('member_nr', '=', member_nr)])

  # Validator

  def _validator_test(self):
    return {}

  def _validator_return_test(self):
    return {'message': {'type': 'string'}}

  def _validator_update_firebase_uid(self):
    res = {
      'member_nr': {'type': 'integer', 'required': True, 'empty': False},
      'uid': {'type': 'string', 'required': True, 'empty': False}
    }
    return res

  def _validator_return_update_firebase_uid(self):
    return {}

  def _validator_get_member_info(self):
    return {
      'uid': {'type': 'string'},
    }

  def _validator_return_get_member_info(self):
    return {}

  def _validator_search(self):
    return {
      'name': {
        'type': 'string',
        'nullable': False,
        'required': True,
      },
    }

  def _validator_return_search(self):
    return {
      'count': {'type': 'integer', 'required': True},
      'rows': {
        'type': 'list',
        'required': True,
        'schema': {
          'type': 'dict',
          'schema': self._validator_return_get()
        }
      }
    }

  def _validator_create(self):
    res = {
      'name': {'type': 'string', 'required': True, 'empty': False},
      'firstname': {'type': 'string', 'required': True, 'empty': False},
      'first_surname': {'type': 'string', 'required': True, 'empty': False},
      'second_surname': {'type': 'string', 'required': True, 'empty': False},

      'dni': {'type': 'string', 'required': True, 'empty': False},
      'birthday': {'type': 'string', 'required': True, 'empty': False},

      'email': {'type': 'string', 'required': True, 'empty': False},
      'phone': {'type': 'string', 'nullable': True, 'empty': False},
      'phone_2': {'type': 'string', 'nullable': True, 'empty': False},

      'iban_1': {'type': 'string', 'required': True, 'empty': False},
      'iban_2': {'type': 'string', 'required': True, 'empty': False},
      'iban_3': {'type': 'string', 'required': True, 'empty': False},
      'iban_4': {'type': 'string', 'required': True, 'empty': False},
      'iban_5': {'type': 'string', 'required': True, 'empty': False},
      'iban_6': {'type': 'string', 'required': True, 'empty': False},

      # 'member_nr': {'type': 'integer', 'required': True, 'empty': False},

      'cooperative_member': {'type': 'string', 'required': True, 'empty': False},
      'register_carsharing': {'type': 'string', 'required': True, 'empty': False},
      'membership_success': {'type': 'string', 'required': True, 'empty': False},

      'street': {'type': 'string', 'required': True, 'empty': False},
      'street2': {'type': 'string', 'nullable': True},
      'zip': {'type': 'string', 'required': True, 'empty': False},
      # 'state': {'type': 'string', 'required': True, 'empty': False},
      'city': {'type': 'string', 'required': True, 'empty': False},

    }
    return res

  def _validator_return_create(self):
    return {}

  def _validator_update(self):
    res = self._validator_create()
    for key in res:
      if 'required' in res[key]:
        del res[key]['required']
    return res

  def _validator_return_update(self):
    return self._validator_return_get()

  def _validator_archive(self):
    return {}

  def _validator_get_num_member(self):
    return {}

  def _validator_return_get_num_member(self):
    return {'num_socis': {'type': 'integer'}}

  def _to_json(self, partner):
    res = {
      'id': partner.member_nr,
      'name': partner.firstname,
      'first_surname': partner.first_surname,
      'second_surname': partner.second_surname,
      'birthday': partner.birthday,
      'street': partner.street,
      'zip': partner.zip,
      'city': partner.computed_city,
      'province': partner.computed_state,
      'phone1': partner.phone,
      'phone2': partner.phone_2,
      'email': partner.email,
      'dni': partner.dni,
      'member_nr': partner.member_nr,
      # 'cs_pocketbook': partner.cs_pocketbook,
      'iban1': partner.iban_1,
      'iban2': partner.iban_2,
      'iban3': partner.iban_3,
      'iban4': partner.iban_4,
      'iban5': partner.iban_5,
      'iban6': partner.iban_6,
      'invoice_email': partner.invoicing_email

    }
    if partner.country_id:
      res['country'] = {
        'id': partner.country_id.id,
        'name': partner.country_id.name
      }
    if partner.state_id:
      res['state'] = {
        'id': partner.state_id.id,
        'name': partner.state_id.name
      }
    return res

  def _validator_update_general_info(self):
    res = {
      'uid': {'type': 'string', 'required': True, 'empty': False},
      "name": {'type': 'string', 'required': True, 'empty': False},
      "first_surname": {'type': 'string', 'required': True, 'empty': False},
      "second_surname": {'type': 'string', 'required': True, 'empty': False},
      "birthday": {'type': 'string', 'required': True, 'empty': False},
      "dni": {'type': 'string', 'required': True, 'empty': False},
      "FBA_SESSION_ID": {'type': 'string', 'required': False, 'empty': True}
    }
    return res

  def _validator_return_update_general_info(self):
    return {}

  def _validator_update_address_info(self):
    res = {
      'uid': {'type': 'string', 'required': True, 'empty': False},
      "street": {'type': 'string', 'required': True, 'empty': False},
      "zip": {'type': 'string', 'required': True, 'empty': False},
      "city": {'type': 'string', 'required': True, 'empty': False},
      "province": {'type': 'string', 'required': True, 'empty': False},
      "FBA_SESSION_ID": {'type': 'string', 'required': False, 'empty': True}
    }
    return res

  def _validator_return_update_address_info(self):
    return {}

  def _validator_update_payment_info(self):
    res = {
      'uid': {'type': 'string', 'required': True, 'empty': False},
      "iban1": {'type': 'string', 'required': True, 'empty': False},
      "iban2": {'type': 'string', 'required': True, 'empty': False},
      "iban3": {'type': 'string', 'required': True, 'empty': False},
      "iban4": {'type': 'string', 'required': True, 'empty': False},
      "iban5": {'type': 'string', 'required': True, 'empty': False},
      "iban6": {'type': 'string', 'required': True, 'empty': False},
      "invoice_email": {'type': 'string', 'required': True, 'empty': False},
      "FBA_SESSION_ID": {'type': 'string', 'required': False, 'empty': True}
    }
    return res

  def _validator_return_update_payment_info(self):
    return {}

  def _validator_update_contact_info(self):
    res = {
      'uid': {'type': 'string', 'required': False, 'empty': False},
      "phone1": {'type': 'string', 'required': True, 'empty': False},
      "phone2": {'type': 'string', 'required': True, 'empty': False},
      "email": {'type': 'string', 'required': True, 'empty': False},
      "FBA_SESSION_ID": {'type': 'string', 'required': False, 'empty': True}
    }
    return res

  def _validator_return_update_contact_info(self):
    return {}

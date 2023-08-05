# -*- coding: utf-8 -*-


from odoo.addons.sm_rest_api.models.models import validate_request
from odoo.addons.base_rest.controllers import main
from odoo.http import Controller, ControllerType, Response, request, route


class PartnerRestPublicApiController(main.RestController):
  _root_path = '/partners/public/'
  _collection_name = 'partner.rest.public.services'
  _default_auth = 'public'

  @route([
    _root_path + '<string:_service_name>/test/<int:_id>'
  ], methods=['GET'], auth="public", csrf=False)
  def test(self, _service_name, _id=None, **params):
    return self._process_method(_service_name, 'test', _id, params)

  @validate_request
  @route([
    _root_path + '<string:_service_name>/update_firebase_uid'
  ], methods=['POST'], auth="public", csrf=False)
  def update_firebase_uid(self, _service_name, _id=None, **params):
    return self._process_method(_service_name, 'update_firebase_uid', _id, params)

  @route([
    _root_path + '<string:_service_name>/member_number'
  ], methods=['GET'], auth="public", csrf=False)
  def get_num_member(self, _service_name, _id=None, **params):
    return self._process_method(_service_name, 'get_num_member', _id, params)

  @validate_request
  @route([
    _root_path + '<string:_service_name>/member_info'
  ], methods=['GET'], auth="public", csrf=False)
  def get_member_info(self, _service_name, _id=None, **params):
    return self._process_method(_service_name, 'get_member_info', _id, params)

  @validate_request
  @route([
    _root_path + '<string:_service_name>/update_general_info'
  ], methods=['POST'], auth="public", csrf=False)
  def get_member_info(self, _service_name, _id=None, **params):
    return self._process_method(_service_name, 'update_general_info', _id, params)

  @validate_request
  @route([
    _root_path + '<string:_service_name>/update_address_info'
  ], methods=['POST'], auth="public", csrf=False)
  def get_member_info(self, _service_name, _id=None, **params):
    return self._process_method(_service_name, 'update_address_info', _id, params)

  @validate_request
  @route([
    _root_path + '<string:_service_name>/update_payment_info'
  ], methods=['POST'], auth="public", csrf=False)
  def get_member_info(self, _service_name, _id=None, **params):
    return self._process_method(_service_name, 'update_payment_info', _id, params)

  @validate_request
  @route([
    _root_path + '<string:_service_name>/update_contact_info'
  ], methods=['POST'], auth="public", csrf=False)
  def get_member_info(self, _service_name, _id=None, **params):
    return self._process_method(_service_name, 'update_contact_info', _id, params)

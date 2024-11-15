# ----------------------------------------------------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------------------------------------------------
from typing import Union
from copy import deepcopy as external_deep_copy

from web_request import WebRequest, HTTPBasicAuth


# ----------------------------------------------------------------------------------------------------------------------
# Classes
# ----------------------------------------------------------------------------------------------------------------------

class RestAPIClient:

  class Exception(Exception):
    pass

  def __init__(self, web_request: WebRequest = WebRequest(), base_url: str = "",
               default_params: dict = None,
               default_headers: dict = None, default_data: dict = None):
    self.default_params = {}
    if default_params:
      self.default_params = default_params
    self.default_headers = {}
    if default_headers:
      self.default_headers = default_headers
    self.default_data = {}
    if default_data:
      self.default_data = default_data

    self.web_request = web_request
    self.default_params = {}
    self.base_url = base_url

  def __try_raise_exception(self, function_to_call: callable, message: str = ""):
    try:
      return function_to_call()
    except Exception as e:
      raise self.Exception(message) from e

  @classmethod
  def __combine_with_default_data(cls, item1: dict = None, item2: dict = None) -> dict:
    if item1 is None:
      item1 = {}
    if item2 is None:
      item2 = {}
    result = cls.copy_without_keeping_reference(item1)
    result.update(item2)
    return result
  @classmethod
  def copy_without_keeping_reference(cls, source_dict_or_list: Union[dict, list]):
    return external_deep_copy(source_dict_or_list)

  def __send_json_request(self, url: str, params: dict, data: dict, headers: dict, function_to_trigger: callable,
                          form_to_json=False, auth: HTTPBasicAuth = None):
    if data is None:
      data = {}
    if headers is None:
      headers = {}

    def function_to_call():
      result = {}
      params_to_send = self.__combine_with_default_data(item1=self.default_params, item2=params)
      data_to_send = self.__combine_with_default_data(item1=self.default_data, item2=data)
      headers_to_send = self.__combine_with_default_data(item1=self.default_headers, item2=headers)
      final_url = self.base_url + url
      response_data = function_to_trigger(url=final_url, params=params_to_send, data=data_to_send,
                                          headers=headers_to_send, form_to_json=form_to_json, auth=auth)
      response_data.raise_for_status()
      if response_data.content != b'':
        result = response_data.json()
      return result

    return self.__try_raise_exception(function_to_call=function_to_call,
                                      message="Cannot get Json data from url \"{}\"".format(url))

  def get_json(self, url: str, params: dict = None, data: dict = None, headers: dict = None,
               auth: HTTPBasicAuth = None):
    return self.__send_json_request(url=url, params=params, data=data, headers=headers,
                                    function_to_trigger=self.web_request.get, auth=auth)

  def post_json(self, url: str, params: dict = None, data: dict = None, headers: dict = None, form_to_json=False,
                auth: HTTPBasicAuth = None):
    return self.__send_json_request(url=url, params=params, data=data, headers=headers,
                                    function_to_trigger=self.web_request.post, form_to_json=form_to_json, auth=auth)

  def put_json(self, url: str, params: dict = None, data: dict = None, headers: dict = None,
               auth: HTTPBasicAuth = None):
    return self.__send_json_request(url=url, params=params, data=data, headers=headers,
                                    function_to_trigger=self.web_request.put, auth=auth)

  def delete_json(self, url: str, params: dict = None, data: dict = None, headers: dict = None,
                  auth: HTTPBasicAuth = None):
    return self.__send_json_request(url=url, params=params, data=data, headers=headers,
                                    function_to_trigger=self.web_request.delete, auth=auth)


  @classmethod
  def build_data(cls, values: dict, add_this_key_if_it_is_empty: list = None) -> dict:
    if add_this_key_if_it_is_empty is None:
      add_this_key_if_it_is_empty = []
    result = {}
    for key, value in values.items():
      if key in add_this_key_if_it_is_empty or value:
        result[key] = value
    return result

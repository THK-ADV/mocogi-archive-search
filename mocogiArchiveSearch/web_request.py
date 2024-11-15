# ----------------------------------------------------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------------------------------------------------
import jsons
import requests
from requests.auth import HTTPBasicAuth
# ----------------------------------------------------------------------------------------------------------------------
# Classes
# ----------------------------------------------------------------------------------------------------------------------
class WebRequest:

  class Exception(Exception):
    pass

  def __init__(self, verify=None):
    self.session = requests.Session()
    self.verify = verify

  def __try_raise_exception(self, function_to_call: callable, message: str = ""):
    try:
      return function_to_call()
    except Exception as e:
      raise self.Exception(message) from e

  def __set_verify(self, verify):
    result = self.verify
    if self.verify is None:
      result = verify
    return result

  def __send_request(self, url, function_to_trigger: callable, params=None, data=None, headers=None, verify=True,
                     auth: HTTPBasicAuth = None):
    result = None
    verify = self.__set_verify(verify)

    def function_to_call():
      nonlocal result

      query_string = '&'.join([f"{key}={value}" for key, value in params.items()])

      full_url = f"{url}?{query_string}"

      result = function_to_trigger(url=full_url, headers=headers, data=data, verify=verify, auth=auth)
      return result

    return self.__try_raise_exception(function_to_call=function_to_call,
                                      message="Cannot get Data from url \"{}\"".format(url))

  def get(self, url, params=None, data=None, headers=None, verify=True, form_to_json=False,
          auth: HTTPBasicAuth = None):
    if form_to_json:
      data = jsons.dumps(data)
    return self.__send_request(url=url, function_to_trigger=self.session.get, params=params,
                               data=data, headers=headers, verify=verify, auth=auth)

  def post(self, url, params=None, data=None, headers=None, verify=True, form_to_json=False,
           auth: HTTPBasicAuth = None):
    if form_to_json:
      data = jsons.dumps(data)
    return self.__send_request(url=url, function_to_trigger=self.session.post, params=params,
                               data=data, headers=headers, verify=verify, auth=auth)

  def put(self, url, params=None, data=None, headers=None, verify=True, form_to_json=False,
          auth: HTTPBasicAuth = None):
    if form_to_json:
      data = jsons.dumps(data)
    return self.__send_request(url=url, function_to_trigger=self.session.put, params=params,
                               data=data, headers=headers, verify=verify, auth=auth)

  def delete(self, url, params=None, data=None, headers=None, verify=True, form_to_json=False,
             auth: HTTPBasicAuth = None):
    if form_to_json:
      data = jsons.dumps(data)
    return self.__send_request(url=url, function_to_trigger=self.session.delete, params=params,
                               data=data, headers=headers, verify=verify, auth=auth)

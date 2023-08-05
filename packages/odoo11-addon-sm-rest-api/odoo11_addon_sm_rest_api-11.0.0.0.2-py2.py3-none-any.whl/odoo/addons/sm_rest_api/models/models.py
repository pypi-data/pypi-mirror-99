# -*- coding: utf-8 -*-

import functools

from firebase_admin import auth as auth_firebase
from odoo import http
from odoo.addons.sm_connect.models.models_sm_carsharing_db_utils import sm_carsharing_db_utils
from odoo.http import Response

_db_utils = sm_carsharing_db_utils.get_instance()


def validate_request(func):
  @functools.wraps(func)
  def wrapper(self, *a, **kw):
    try:
      request = http.request
      http_request = request.httprequest
      request_headers = http_request.headers
      header_environ = request_headers.environ

      if 'HTTP_FBA_SESSION_ID' in header_environ:
        session_id = header_environ['HTTP_FBA_SESSION_ID']
        if session_id == '':
          return Response("Empty session token provided", status=401)
        decoded_token = auth_firebase.verify_id_token(session_id)
        kw['uid'] = decoded_token['uid']

      elif 'FBA_SESSION_ID' in kw:
        decoded_token = auth_firebase.verify_id_token(kw['FBA_SESSION_ID'])
        kw['uid'] = decoded_token['uid']
      else:
        return Response("No token provided", status=401)

    except:
      return Response("Invalid validation", status=401)

    return func(self, *a, **kw)

  return wrapper

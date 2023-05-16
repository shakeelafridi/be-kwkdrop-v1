import json

from django.http import HttpResponse

from .constants import *


class SuccessResponse:
    def __init__(self, data=None, message='', status_code=SUCCESS_RESPONSE_CODE):
        if data is None:
            data = {}
        self.data = data
        self.message = message
        self.status_code = status_code

    def response_object(self):
        return {
            'data': self.data,
            'meta': {'status_code': self.status_code, 'message': self.message}
        }

    def return_response_object(self):
        try:
            value_ = json.dumps(self.response_object())
            return respond(value_, self.status_code)
        except Exception as e:
            return FailureResponse('Failed to serialize data').return_response_object()


class FailureResponse:
    def __init__(self, message='Something Went Wrong', status_code=INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code

    def response_object(self):
        return {
            'data': {},
            'meta': {'status_code': self.status_code, 'message': self.message}
        }

    def response_object_bad_request(self):
        self.status_code = BAD_REQUEST_CODE
        return {
            'data': {},
            'meta': {'status_code': self.status_code, 'message': self.message}
        }

    def method_not_allowed(self):
        self.status_code = METHOD_NOT_ALLOWED
        dict_ = {
            'data': {},
            'meta': {'status_code': METHOD_NOT_ALLOWED, 'message': 'Method Not Allowed'}
        }
        return respond(json.dumps(dict_), METHOD_NOT_ALLOWED)

    def unauthorized_object(self):
        self.status_code = UNAUTHORIZED
        dict_ = {
            'data': {},
            'meta': {'status_code': UNAUTHORIZED, 'message': 'Unauthorized User'}
        }
        return respond(json.dumps(dict_), UNAUTHORIZED)

    def return_response_object(self):
        return respond(json.dumps(self.response_object()), self.status_code)


def respond(value, status):
    response = HttpResponse(value, content_type='application/json', status=status)
    return response

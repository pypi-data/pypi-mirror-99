import json
from flask import request, g


def get_request_user():
    return g.request_user


def get_request_session():
    return g.session


def get_request_method():
    return request.method


def get_request_headers(key=None, default=''):
    if key:
        if request.headers:
            return request.headers.get(key, default)
        else:
            return default
    else:
        if request.headers:
            return request.headers
        else:
            if default != '':
                return default
            else:
                return {}


def get_request_data(key=None, default=''):
    if key:
        if request.data:
            return json.loads(request.data).get(key, default)
        else:
            return default
    else:
        if request.data:
            return json.loads(request.data)
        else:
            if default != '':
                return default
            else:
                return {}


def get_request_args(key=None):
    if key:
        return request.args.get(key)
    else:
        return request.args


def get_request_url():
    return request.url

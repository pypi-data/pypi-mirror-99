# coding:utf-8
import json
import requests
from flask import request
from dotdict import DotDict
from webcore import constant
from webcore import exception

def post(url, headers={}, data=None, json=None):
    _set_auth_header(headers)
    response = requests.post(
        url, 
        headers=headers, 
        json=json,
        data=data,
        verify=False)
    return _get_response_data(response)

def get(url, headers={}, params=None):
    _set_auth_header(headers)
    response = requests.get(
        url, 
        headers=headers, 
        params=params,
        verify=False)

    return _get_response_data(response)

def put(url, headers={}, data=None):
    _set_auth_header(headers)
    response = requests.put(
        url, 
        headers=headers,
        data=data,
        verify=False)
    return _get_response_data(response)

def delete(url, headers={}, params=None):
    _set_auth_header(headers)
    response = requests.delete(
        url, 
        headers=headers, 
        params=params, 
        verify=False)
    return _get_response_data(response)
    
def _set_auth_header(headers):
    token = request.headers.get('Authorization')
    headers['Authorization'] = token

def _get_response_data(response):
    result = DotDict(response.json())

    if result.code != constant.Error.OK.value:
        raise exception.GtBaseError(result.code, result.msg)

    return result.data

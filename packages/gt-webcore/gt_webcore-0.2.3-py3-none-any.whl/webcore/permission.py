# -*- coding: utf-8 -
from flask import current_app as app
from flask import request, g
from webcore.constant import Error
from webcore import exception
from webcore import http_request
import functools

def check_perm(action='', resource={}, context={}):
    """
    权限判断
    :param action: 动作，字符串表示函数标识，字典表示动作属性
    :param resource: 资源
    :param context: 环境，默认会传请求ip
    """
    if isinstance(action, str):
        action = { 'method': action }

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            system_id = app.config['SYSTEM_ID']
            auth_url = app.config['AUTH_URL']

            if not system_id:
                raise exception.ParamsError('没有配置系统标识')

            if not auth_url:
                raise exception.ParamsError('没有配置授权服务地址')

            payload = http_request.post(auth_url, json = {
                'system_id': system_id,
                'token': token,
                'action': action,
                'resource': resource,
                'context': dict(context, ip=request.remote_addr)
            })

            if not payload:
                raise exception.GtBaseError(Error.AUTHOR_ERROR, '没有访问授权')

            g.__dict__.update(payload)
            return func(*args, **kwargs)

        return wrapper
    return decorator

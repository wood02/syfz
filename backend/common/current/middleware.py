# -*- coding: utf-8 -*-
import datetime
import json
import re
import time

from django.db import transaction
from django.db.models import Q
from django.utils.deprecation import MiddlewareMixin

from apps.system.models import LoginEvent, Modular, OperationLog
from apps.user.models import User
from common.utils.request_util import *
from Syfz import settings

"""
请求(Request)中间件->对应函数process_request
视图(View)中间件->对应函数process_view
模板(Template)中间件->对应函数process_template_response（不常用）
响应(Response)中间件->对应函数process_response
异常(Exception)中间件->对应函数process_exception（不常用）
"""


class LoginEventMiddleware(MiddlewareMixin):
    """
    登录日志
    """
    LOGIN_URL = ["/api/user/login/"]

    @classmethod
    def __handle_request(cls, request):
        request.request_ip = get_request_ip(request)
        request.request_data = get_request_data(request)
        request.request_path = get_request_path(request)

    def process_request(self, request):
        self.__handle_request(request)

    def process_response(self, request, response):
        """
        登录日志
        :param response:
        :param request:
        :return:
        """
        body = getattr(request, 'request_data', {})
        user = User.objects.filter(username=body.get("username")).first()
        if get_request_path(request) in self.LOGIN_URL:
            last_login = None
            if response.data.get("code") == 200:
                login_status = 1
                password = '*' * len(body['password'])
                if user:
                    last_login = user.last_login
            else:
                login_status = 2
                password = body.get("password")

            with transaction.atomic():
                data = {
                    'username': body.get("username"),
                    'password': password,
                    'user_id': getattr(user, 'id', None),
                    'login_ip': get_request_ip(request),
                    'os_type': get_os(request),
                    'browser_type': get_browser(request),
                    'terminal_type': get_get_device(request),  # 终端类型
                    'equipment_name': None,  # 设备名称
                    'is_super': False,
                    'login_date': last_login,
                    'login_status': login_status,

                    # 'mac_address': getattr(request.data, "mac_address", None),  # MAC
                }
                LoginEvent.objects.create(**data)
        return response


class ApiLoggingMiddleware(MiddlewareMixin):
    """
    用于记录API访问日志中间件
    """

    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.enable = getattr(settings, 'API_LOG_ENABLE', None) or False
        self.methods = getattr(settings, 'API_LOG_METHODS', None) or set()

    @classmethod
    def __handle_request(cls, request):
        request.request_ip = get_request_ip(request)
        request.request_data = get_request_data(request)
        request.request_path = get_request_path(request)

    @classmethod
    def __handle_response(cls, request, response):
        url_path = ReID(request.request_path)
        m = Modular.objects.filter(Q(url_path=url_path), Q(method=request.method)).first()
        # 过滤掉加入数据库并且标准为不显示的
        if m.is_show or not m:
            modular_name = m.modular_name if m else None
            handle_type = m.handle_type if m else None
            # 判断已知类型
            # 处理不是 api
            if request.request_path.startswith("/api/"):
                # request_data,request_ip由PermissionInterfaceMiddleware中间件中添加的属性
                body = getattr(request, 'request_data', {})
                # 请求含有password则用*替换掉(暂时先用于所有接口的password请求参数)
                if isinstance(body, dict) and body.get('password', ''):
                    body['password'] = '*' * len(body['password'])
                if not hasattr(response, 'data') or not isinstance(response.data, dict):
                    response.data = {}
                if not response.data and response.content:
                    try:
                        content = json.loads(response.content.decode())
                        response.data = content if isinstance(content, dict) else {}
                    except:
                        pass
                body = json.dumps(body, ensure_ascii=False)
                json_result = {"code": response.data.get('code'), "success": response.data.get('success', True),
                               "message": response.data.get('message')}
                response_data = json.dumps(json_result, ensure_ascii=False)

                user = get_request_user(request)
                user = user if not isinstance(user, AnonymousUser) else None
                info = {
                    'request_ip': get_request_ip(request),
                    'handle_user': user,
                    'request_method': request.method,
                    'request_path': request.request_path,
                    'request_body': body,
                    'response_code': response.data.get('code'),
                    # 'request_location': get_login_location(request),
                    'request_os': get_os(request),
                    'request_browser': get_browser(request),
                    'request_msg': request.session.get('request_msg'),
                    # 'status': True if response.data.get('code') in [200, 204] else False,
                    'status': True if response.data.get('success') else False,
                    'response_data': response_data,
                    'request_modular': modular_name,
                    'handle_type': handle_type,
                }
                # print(info)
                log = OperationLog(**info)
                log.save()

    def process_view(self, request, view_func, view_args, view_kwargs):
        if hasattr(view_func, 'cls') and hasattr(view_func.cls, 'queryset'):
            request.session['model_name'] = get_verbose_name(view_func.cls.queryset)
        return

    def process_request(self, request):
        self.__handle_request(request)

    def process_response(self, request, response):
        """
        主要请求处理完之后记录
        :param request:
        :param response:
        :return:
        """
        if self.enable:
            if self.methods == 'ALL' or request.method in self.methods:
                try:
                    self.__handle_response(request, response)
                except AttributeError:
                    pass
        return response

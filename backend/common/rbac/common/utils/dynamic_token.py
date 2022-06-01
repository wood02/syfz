import re

import pyotp
import requests
from rest_framework import status
from rest_framework.response import Response

from common.rbac.common.utils.customize import make_response
from apps.rbac.models import TokenAuth, GlobalConfig, Users
from common.rbac.common.utils.time_utils import TimeUtils


def generate_secret():
    """
    生成用户绑定用的私钥，一位用户只能绑定一个私钥
    """
    secret = pyotp.random_base32()  # 获取随机密钥，存于用户表中
    return secret


def generate_token(secret):
    """
    生成动态令牌
    secret: 用户私钥
    return: 六位动态令牌
    """
    totp = pyotp.TOTP(secret, interval=60)
    return totp.now()


def check_token(secret, token):
    """
    校验动态令牌
    secret: 用户私钥
    token: 动态令牌
    return: 校验结果(True/False)
    """
    totp = pyotp.TOTP(secret, interval=60)
    return totp.verify(token)


def check_dynamic_token(func):
    def wrapper(*args, **kwargs):
        request = args[1]
        url_path = request.path_info  # 获取接口地址
        url_path = re.sub('/\d+', '', url_path)  # 有些接口带有pk参数，需要去掉pk参数
        method = request.method  # 获取请求方式
        user = request.user
        # 第一步：校验当前接口令牌验证是否开启
        token_auth_query = TokenAuth.objects.filter(url_path=url_path, method=method).first()
        if token_auth_query is None:
            return Response(make_response([], "此接口未开放令牌权限。", 403))
        is_open = token_auth_query.status
        if is_open == "0":
            return func(*args, **kwargs)
        # 第二步：校验当前用户是否开启令牌验证权限
        is_token_open = user.role.filter(permission__url_path="/api/user/", permission__method="POST").count()
        if is_token_open == 0:
            return Response(make_response([], "此用户未开启令牌权限。", 403))
        # 第三步：校验此用户令牌的有效期
        secret = request.user.key
        cst_expired = TimeUtils.dt_to_str(request.user.cst_expired)
        today_time = TimeUtils.get_today_time_str()  # 当前时间
        is_expired = TimeUtils.time1_ge_time2(cst_expired, today_time)
        dynamic_token = request.GET.get("dynamic_token")
        if is_expired:
            # 在有效期内
            return func(*args, **kwargs)
        # 不在有效期内
        if dynamic_token is not None:
            check_result = check_token(secret, dynamic_token)
            if check_result:
                # 验证通过，用户令牌有效期增加
                token_valid_period = GlobalConfig.objects.get(conf_key="token_valid_period").conf_value  # 获取有效期
                now = TimeUtils.get_today_datetime()
                new_cst_expired = TimeUtils.time_add_together(now, int(token_valid_period), 2)
                user.cst_expired = new_cst_expired
                user.save()
                return func(*args, **kwargs)
            else:
                return Response(make_response([], "令牌校验失败", 403))
        else:
            return Response(make_response([], "获取令牌失败", 400))

    return wrapper

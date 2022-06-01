# -*- coding: utf-8 -*-
import datetime
import re
from rest_framework import exceptions, serializers

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.core.cache import cache
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.views import TokenObtainPairView

# from common.drf.simplejwt.serializers import TokenObtainPairSerializer
from common.drf.response import Response


def check_captcha(value):
    """
    验证码校验
    :param value: 验证码
    :return: 校验结果
    """
    pattern = re.compile(r"[a-zA-Z0-9]{4}")
    result = len(pattern.findall(value))
    if len(value) != 4 or result == 0:
        raise serializers.ValidationError("验证码格式不正确")


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 添加自定义校验字段
        self.fields['key'] = serializers.CharField()
        self.fields['captcha'] = serializers.CharField(validators=[check_captcha])

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['secret'] = user.secret.urn
        # ...
        return token

    def validate(self, attrs):
        # 校验验证码
        key = attrs['key']
        captcha = attrs['captcha']
        redis_captcha = cache.get(key, default=None, version=None)
        if redis_captcha is None:
            raise serializers.ValidationError({"captcha": "验证码失效"})
        if captcha.upper() != redis_captcha.upper():
            raise serializers.ValidationError({"captcha": "验证码错误"})
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
        }

        self.user = authenticate(**authenticate_kwargs)
        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                "用户名或密码错误",
                'no_active_account',
            )

        refresh = self.get_token(self.user)
        data = {
            'code': 200, 'success': True, 'message': "登录成功",
            'data': {
                'username': self.user.username,
                'last_login': self.user.last_login.strftime('%Y-%m-%d %H:%M:%S') if self.user.last_login else None,
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }}

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

import time
from django.utils import timezone
import datetime
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication, jwt_decode_handler

from apps.rbac.models import Roles


# class RoleSerializer(serializers.ModelSerializer):
#     """
#     序列化角色
#     """
#
#     class Meta:
#         model = Roles
#         fields = ['role_name']
#
#
# def get_max_role(data):
#     role_list = []
#     for i in data:
#         role_list.append(i['role_name'])
#     if "审计管理员" in role_list:
#         return "审计管理员"
#     if "普通管理员" in role_list:
#         return "普通管理员"
#     if "普通用户" in role_list:
#         return "普通用户"
#     return None


def jwt_payload_handler(user):
    """自定义payload内容"""
    # 用户组信息，用于认证和授权
    return {
        'user_id': user.id,
        'username': user.nick_name,
        'user_secret': user.user_secret.urn  # uuid对象需要处理
    }


def jwt_response_payload_handler(token, user=None, request=None):
    """自定义登录成功后的返回信息，是给前端的"""
    user.last_login = datetime.datetime.now()
    user.save()
    # role = user.role.all()
    # roles = RoleSerializer(role, many=True)
    # role_data = roles.data
    # role = get_max_role(role_data)

    return {
        'username': user.nick_name,
        'last_login': user.last_login,
        'token': token,
        # 'role': role,
    }

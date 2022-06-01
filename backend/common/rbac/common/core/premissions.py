import json
import re
from rest_framework.permissions import BasePermission
from apps.rbac.models import *
from rest_framework import exceptions


class CustomizeViewPermission(BasePermission):
    """自定义视图权限类"""

    def has_permission(self, request, view):
        """
        1)根据需求，request和view的辅助，制定权限规则判断条件，针对整个视图
        2)如果条件通过，返回True
        3)如果条件不通过，返回False
        """
        user = request.user
        url_path = request.path_info  # 获取接口地址
        # 有些接口带有pk参数，需要去掉pk参数
        url_path = re.sub('/\d+', '', url_path)
        method = request.method  # 获取请求方式
        # 判断当前用户是否拥有角色
        try:
            is_role = user.role.all().count()
            if is_role == 0:
                raise exceptions.PermissionDenied("用户不存在角色。", 403)
            # 判断当前用户是否拥有权限
            is_permission = user.role.filter(permission__url_path=url_path, permission__method=method).count()
        except AttributeError:

            return False
        # return True
        return is_permission

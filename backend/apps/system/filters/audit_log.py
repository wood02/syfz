# -*- coding: utf-8 -*-
from django_filters import rest_framework as filters

from apps.system.models import LoginEvent, OperationLog


class LoginEventFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name="id", lookup_expr="exact", label="编号")
    slogin_date = filters.DateTimeFilter(field_name='login_date', lookup_expr='gte', label="开始时间")
    elogin_date = filters.DateTimeFilter(field_name='login_date', lookup_expr='lte', label="结束时间")
    username = filters.CharFilter(field_name="username", lookup_expr="icontains", label="用户名")
    login_ip = filters.CharFilter(field_name="login_ip", lookup_expr="icontains", label="登录IP")
    login_status = filters.NumberFilter(field_name="login_status", lookup_expr="exact", label="登录状态")

    class Meta:
        model = LoginEvent
        fields = ["id", "login_date"]


class OperationLogFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name="id", lookup_expr="exact", label="编号")
    screated_ate = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte', label="开始时间")
    ecreated_at = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte', label="结束时间")
    request_modular = filters.CharFilter(field_name="request_modular", lookup_expr="icontains", label="请求模块")
    request_method = filters.CharFilter(field_name="request_method", lookup_expr="icontains", label="请求方式")
    handle_type = filters.NumberFilter(field_name="handle_type", lookup_expr="icontains", label="操作类型")

    class Meta:
        model = OperationLog
        fields = ["id", "created_at"]

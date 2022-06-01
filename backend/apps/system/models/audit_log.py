# -*- coding: utf-8 -*-
# 审计日志
from django.conf import settings

from apps.user.models import User
from common.django.basemodel import BaseModel
from django.db import models


class LoginEvent(BaseModel):
    LOGIN_STATUS = (
        (0, '未知'),
        (1, '登录成功'),
        (2, '登录失败'),
    )
    username = models.CharField("用户名", max_length=255, null=True, blank=True, db_index=True)
    password = models.CharField("密码", max_length=255, null=True, blank=True)
    login_date = models.DateTimeField("登录时间", null=True, blank=True, db_index=True)
    login_status = models.SmallIntegerField("登录状态", default=1, choices=LOGIN_STATUS, db_index=True)
    terminal_type = models.CharField("终端类型", max_length=50, null=True, blank=True)
    browser_type = models.CharField("浏览器类型", max_length=50, null=True, blank=True)
    os_type = models.CharField("操作系统", max_length=255, null=True, blank=True)
    equipment_name = models.CharField("设备名称", max_length=50, null=True, blank=True)
    mac_address = models.CharField("MAC地址", max_length=50, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                             on_delete=models.SET_NULL, related_name="login_event_user", db_constraint=False)
    login_ip = models.CharField("登录IP", max_length=50, null=True, db_index=True)
    is_super = models.BooleanField("是否是超级用户", default=False)

    def __str__(self):
        return f"{self.username}[{self.login_date}][{self.login_ip}]"

    class Meta:
        db_table = 'syfz_sys_login_event'
        verbose_name = '登录记录'
        verbose_name_plural = verbose_name
        ordering = ['-id']


# 审计日志
class OperationLog(BaseModel):
    request_modular = models.CharField(max_length=64, verbose_name="请求模块", null=True, blank=True)
    request_path = models.CharField(max_length=400, verbose_name="请求地址", null=True, blank=True)
    request_body = models.TextField(verbose_name="请求参数", null=True, blank=True)
    request_method = models.CharField(max_length=64, verbose_name="请求方式", null=True, blank=True)
    request_msg = models.TextField(verbose_name="操作说明", null=True, blank=True)
    request_ip = models.CharField(max_length=32, verbose_name="请求ip地址", null=True, blank=True)
    request_browser = models.CharField(max_length=64, verbose_name="请求浏览器", null=True, blank=True)
    request_location = models.CharField(max_length=64, verbose_name="操作地点", null=True, blank=True)
    request_os = models.CharField(max_length=64, verbose_name="操作系统", null=True, blank=True)
    response_code = models.CharField(max_length=32, verbose_name="响应状态码", null=True, blank=True)
    response_data = models.TextField(verbose_name="返回信息", null=True, blank=True)
    status = models.BooleanField(default=False, verbose_name="响应状态")
    handle_type = models.CharField(max_length=20, verbose_name="操作类型", null=True, blank=True)
    handle_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'syfz_sys_operation_log'
        verbose_name = '操作日志'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return f"{self.id}.{self.request_modular}[{self.created_at}][{self.handle_type}]"


class Modular(BaseModel):
    """请求对应模块"""
    MethodChoices = (
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('PATCH', 'PATCH'),
        ('DELETE', 'DELETE')
    )
    modular_name = models.CharField('模块名称', max_length=50)
    handle_type = models.CharField(max_length=20, verbose_name="操作类型")
    url_path = models.CharField('接口地址', max_length=255)
    method = models.CharField('请求方式', max_length=10, choices=MethodChoices, default='GET')
    is_show = models.BooleanField("是否显示", default=1)
    remark = models.CharField('备注', max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.id}.{self.modular_name}[{self.method}][{self.handle_type}][{self.url_path}]"

    class Meta:
        db_table = 'syfz_sys_modular'
        ordering = ['-id']
        verbose_name = '请求模块'
        verbose_name_plural = verbose_name

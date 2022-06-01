# -*- coding: utf-8 -*-
from django.core.validators import MinValueValidator
from django.db import models

from common.django.basemodel import BaseModel


class FofaToken(BaseModel):
    STATUS = (
        (0, '未知'),
        (1, '正常'),
        (2, '异常'),
    )
    email = models.CharField("邮箱", max_length=255)
    key = models.CharField("邮箱", max_length=255)
    status = models.PositiveSmallIntegerField("状态", default=0, null=True, blank=True, choices=STATUS)
    error_msg = models.CharField("错误信息", max_length=255, null=True, blank=True)
    error_num = models.IntegerField('异常次数', default=0, validators=[MinValueValidator(0)], help_text="错误次数")
    status_change_at = models.DateTimeField('状态改变时间', null=True, blank=True)
    remark = models.CharField("备注", max_length=255, null=True, blank=True)

    class Meta:
        db_table = "passive_fofa_token"
        verbose_name = "FofaToken"
        verbose_name_plural = verbose_name
        ordering = ['-id']
        unique_together = ('email', 'key')


class XtbApiKey(BaseModel):
    STATUS = (
        (0, '未知'),
        (1, '正常'),
        (2, '异常'),
        (3, '失效'),
    )
    username = models.CharField("用户名", max_length=100, null=True, blank=True)
    apikey = models.CharField("ApiKey", max_length=255, unique=True)
    status = models.PositiveSmallIntegerField("状态", default=0, null=True, blank=True, choices=STATUS)
    error_msg = models.CharField("错误信息", max_length=255, null=True, blank=True)
    error_num = models.IntegerField('异常次数', default=0, validators=[MinValueValidator(0)], help_text="错误次数")
    status_change_at = models.DateTimeField('状态改变时间', null=True, blank=True)

    api_limit = models.IntegerField('API限制', default=50, )
    api_remaining = models.IntegerField('API剩余', default=50, validators=[MinValueValidator(0)])
    api_reset_at = models.DateTimeField('重置时间', null=True, blank=True)
    remark = models.CharField("备注", max_length=255, null=True, blank=True)

    class Meta:
        db_table = "passive_xbt_apikey"
        verbose_name = "XtbApiKey"
        verbose_name_plural = verbose_name
        ordering = ['-id']
        # unique_together = ('username', 'apikey')


class NsfocusApiKey(BaseModel):
    STATUS = (
        (0, '未知'),
        (1, '正常'),
        (2, '异常'),
        (3, '失效'),
    )
    apikey = models.CharField("ApiKey", max_length=255, unique=True)
    status = models.PositiveSmallIntegerField("状态", default=0, null=True, blank=True, choices=STATUS)
    error_msg = models.CharField("错误信息", max_length=255, null=True, blank=True)
    error_num = models.IntegerField('异常次数', default=0, validators=[MinValueValidator(0)], help_text="错误次数")
    status_change_at = models.DateTimeField('状态改变时间', null=True, blank=True)

    api_limit = models.IntegerField('API限制', default=50, )
    api_remaining = models.IntegerField('API剩余', default=50, validators=[MinValueValidator(0)])
    api_reset_at = models.DateTimeField('重置时间', null=True, blank=True)
    remark = models.CharField("备注", max_length=255, null=True, blank=True)

    class Meta:
        db_table = "passive_nsfocus_apikey"
        verbose_name = "NsfocusApiKey"
        verbose_name_plural = verbose_name
        ordering = ['-id']


class ZoomEyeToken(BaseModel):
    STATUS = (
        (0, '未知'),
        (1, '正常'),
        (2, '异常'),
    )
    token = models.CharField("Token", max_length=100, unique=True)
    status = models.PositiveSmallIntegerField("状态", default=0, null=True, blank=True, choices=STATUS)
    rate_limit = models.JSONField("限制信息", default=dict, null=True, blank=True)
    remark = models.CharField("备注", max_length=255, null=True, blank=True)
    error_message = models.TextField("异常信息", null=True, blank=True)

    class Meta:
        db_table = "passive_zoomeye_token"
        verbose_name = "ZoomEye token"
        verbose_name_plural = verbose_name
        ordering = ['-id']

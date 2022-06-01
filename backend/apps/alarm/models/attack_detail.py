# -*- coding: utf-8 -*-
from django.db import models

from common.django.basemodel import BaseModel


class DetailDomain(BaseModel):
    attack = models.ForeignKey(
        'Attack',
        verbose_name='攻击日志',
        related_name='detail_domain',
        on_delete=models.CASCADE
    )
    domain = models.JSONField("备案信息", default=list, null=True, blank=True)

    class Meta:
        db_table = "alarm_detail_domain"
        verbose_name = "攻击详情-域名备案"
        verbose_name_plural = verbose_name
        ordering = ['-id']


class DetailTagInfo(BaseModel):

    SOURCE = (
        (0, '未知'),
        (1, '微步'),
        (2, '绿盟'),
    )
    attack = models.ForeignKey(
        'Attack',
        verbose_name='攻击日志',
        related_name='detail_tag_info',
        on_delete=models.CASCADE
    )
    tag_info = models.JSONField("标签信息", default=dict, null=True, blank=True)
    ports = models.JSONField("端口信息", default=list, null=True, blank=True)
    cur_domains = models.JSONField("domains信息", default=list, null=True, blank=True)
    history_domains = models.JSONField("history_domains信息", default=dict, null=True, blank=True)
    source = models.PositiveSmallIntegerField("来源", default=1, null=True, blank=True, choices=SOURCE)

    class Meta:
        db_table = "alarm_detail_tag_info"
        verbose_name = "攻击详情-标签信息"
        verbose_name_plural = verbose_name
        ordering = ['-id']


class DetailLocation(BaseModel):
    attack = models.ForeignKey(
        'Attack',
        verbose_name='攻击日志',
        related_name='detail_location',
        on_delete=models.CASCADE
    )
    location = models.JSONField("地理位置信息", default=dict, null=True, blank=True)

    class Meta:
        db_table = "alarm_detail_location"
        verbose_name = "攻击详情-地理位置信息"
        verbose_name_plural = verbose_name
        ordering = ['-id']

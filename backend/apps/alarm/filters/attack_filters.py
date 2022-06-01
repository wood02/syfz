#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django_filters import rest_framework as filters

from apps.alarm.models import Attack, AttackWhite


class AttackFilterBackend(filters.DjangoFilterBackend):
    def get_filterset_kwargs(self, request, queryset, view):
        kwargs = super().get_filterset_kwargs(request, queryset, view)

        # merge filterset kwargs provided by view class
        if hasattr(view, 'get_filterset_kwargs'):
            kwargs.update(view.get_filterset_kwargs())

        # 自定义
        queryset = kwargs.get('queryset')
        # 查询会有重复 .distinct() 可去重
        # 需要在 ModelViewSet 加入以下 filter_backends = [AttackFilterBackend]
        kwargs['queryset'] = queryset.distinct()
        return kwargs


class AttackFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name="id", lookup_expr="exact", label="编号")
    sattack_earliest_time = filters.DateTimeFilter(field_name='attack_earliest_time', lookup_expr='gte', label="开始时间")
    eattack_earliest_time = filters.DateTimeFilter(field_name='attack_earliest_time', lookup_expr='lte', label="结束时间")
    source_ip = filters.CharFilter(field_name="source_ip", lookup_expr="icontains", label="策略名")
    destination_ip = filters.CharFilter(field_name="attack_details__destination_ip", lookup_expr="icontains",
                                        label="目的IP")
    source = filters.CharFilter(field_name="attack_details__source", lookup_expr="icontains", label="来源")
    attack_type = filters.CharFilter(field_name="attack_details__attack_type", lookup_expr="icontains", label="攻击类型")
    location = filters.CharFilter(field_name="location", lookup_expr="icontains", label="地理位置")
    intel_types = filters.CharFilter(field_name="intel_types", lookup_expr="icontains", label="IP属性")
    malicious = filters.CharFilter(field_name="malicious", lookup_expr="exact", label="恶意类型")
    fz_status = filters.CharFilter(field_name="fz_status", lookup_expr="exact", label="反制状态")

    class Meta:
        model = Attack
        fields = ["id", "attack_earliest_time", "source_ip"]


class AttackWhiteFilter(filters.FilterSet):
    white_ip = filters.CharFilter(field_name="white_ip", lookup_expr="icontains", label="IP")
    remark = filters.CharFilter(field_name="remark", lookup_expr="icontains", label="备注")

    class Meta:
        model = AttackWhite
        fields = ['white_ip', 'remark']

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django_filters import rest_framework as filters

from apps.tracesource.models import ScanPort, WeakPassword, Vulnerability, DirectoryBlast, WebServer


class ScanPortFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name="id", lookup_expr="exact", label="编号")
    source_ip = filters.CharFilter(field_name='source_ip', lookup_expr='icontains', label="源IP")
    port = filters.CharFilter(field_name='ports', lookup_expr='icontains', label="端口")
    shit_time = filters.DateTimeFilter(field_name='hit_time', lookup_expr='gte', label="开始时间")
    ehit_time = filters.DateTimeFilter(field_name='hit_time', lookup_expr='lte', label="结束时间")

    class Meta:
        model = ScanPort
        fields = ["id", "source_ip", "port", "hit_time"]


class WebServerFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name="id", lookup_expr="exact", label="编号")
    site = filters.CharFilter(field_name='site', lookup_expr='icontains', label="站点")
    title = filters.CharFilter(field_name='title', lookup_expr='icontains', label="标题")
    header = filters.CharFilter(field_name='header', lookup_expr='icontains', label="header")
    fingerprint = filters.CharFilter(field_name='fingerprint', lookup_expr='icontains', label="指纹")
    shit_time = filters.DateTimeFilter(field_name='hit_time', lookup_expr='gte', label="开始时间")
    ehit_time = filters.DateTimeFilter(field_name='hit_time', lookup_expr='lte', label="结束时间")

    class Meta:
        model = WebServer
        fields = ["id", "site", "title", "hit_time", "header", "fingerprint"]


class DirectoryBlastFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name="id", lookup_expr="exact", label="编号")
    host = filters.CharFilter(field_name='host', lookup_expr='icontains', label="host")
    source_ip = filters.CharFilter(field_name='source_ip', lookup_expr='icontains', label="source_ip")
    title = filters.CharFilter(field_name='title', lookup_expr='icontains', label="标题")
    status_code = filters.CharFilter(field_name='search_code_str', lookup_expr='icontains', label="标题")
    dir = filters.CharFilter(field_name='search_dir_str', lookup_expr='icontains', label="标题")
    shit_time = filters.DateTimeFilter(field_name='hit_time', lookup_expr='gte', label="开始时间")
    ehit_time = filters.DateTimeFilter(field_name='hit_time', lookup_expr='lte', label="结束时间")

    class Meta:
        model = DirectoryBlast
        fields = ["id", "host", "source_ip", "title", "hit_time"]


class VulnerabilityFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name="id", lookup_expr="exact", label="编号")
    name = filters.CharFilter(field_name='name', lookup_expr='icontains', label="名称")
    cve_num = filters.CharFilter(field_name='cve_num', lookup_expr='icontains', label="漏洞编号")
    source_ip = filters.CharFilter(field_name='source_ip', lookup_expr='icontains', label="源IP")
    vul_site = filters.CharFilter(field_name='vul_site', lookup_expr='icontains', label="漏洞地址")
    shit_time = filters.DateTimeFilter(field_name='hit_time', lookup_expr='gte', label="开始时间")
    ehit_time = filters.DateTimeFilter(field_name='hit_time', lookup_expr='lte', label="结束时间")

    class Meta:
        model = Vulnerability
        fields = ["id", "name", "cve_num", "source_ip", "vul_site", "hit_time"]


class WeakPasswordFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name="id", lookup_expr="exact", label="编号")
    name = filters.CharFilter(field_name='name', lookup_expr='icontains', label="名称")
    cve_num = filters.CharFilter(field_name='cve_num', lookup_expr='icontains', label="漏洞编号")
    source_ip = filters.CharFilter(field_name='source_ip', lookup_expr='icontains', label="源IP")
    sever = filters.CharFilter(field_name='sever', lookup_expr='icontains', label="服务")
    shit_time = filters.DateTimeFilter(field_name='hit_time', lookup_expr='gte', label="开始时间")
    ehit_time = filters.DateTimeFilter(field_name='hit_time', lookup_expr='lte', label="结束时间")

    class Meta:
        model = WeakPassword
        fields = ["id", "name", "cve_num", "source_ip", "sever", "hit_time"]

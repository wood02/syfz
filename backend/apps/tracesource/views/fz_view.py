import requests
from requests import ReadTimeout
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from apps.alarm.models import Attack
from apps.system.models import GlobalConfig
from apps.tracesource.filters.fz_filter import ScanPortFilter, WebServerFilter, DirectoryBlastFilter, \
    VulnerabilityFilter, WeakPasswordFilter
from apps.tracesource.models.fz import ScanPort, WebServer, DirectoryBlast, Vulnerability, WeakPassword
from apps.tracesource.serializers.fz_ser import (
    ScanPortSerializer,
    WebServerSerializer,
    DirectoryBlastSerializer,
    VulnerabilitySerializer, WeakPasswordSerializer
)
from apps.tracesource.utils.fz_scan import scan
from common.drf.response import Response
from common.drf.viewsets import ModelViewSet


class ScanPortViewSet(ModelViewSet):
    queryset = ScanPort.objects.all()
    serializer_class = ScanPortSerializer
    filter_class = ScanPortFilter


class WebServerViewSet(ModelViewSet):
    queryset = WebServer.objects.all()
    serializer_class = WebServerSerializer
    filter_class = WebServerFilter


class DirectoryBlastViewSet(ModelViewSet):
    queryset = DirectoryBlast.objects.all()
    serializer_class = DirectoryBlastSerializer
    filter_class = DirectoryBlastFilter


class VulnerabilityViewSet(ModelViewSet):
    queryset = Vulnerability.objects.all()
    serializer_class = VulnerabilitySerializer
    filter_class = VulnerabilityFilter


class WeakPasswordViewSet(ModelViewSet):
    queryset = WeakPassword.objects.all()
    serializer_class = WeakPasswordSerializer
    filter_class = WeakPasswordFilter


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def callback(request, format=None):
    """
    接收来自fz的数据
    :param request:
    :param format:
    :return:
    """
    data = request.data

    return Response(success=True, data=[], message='success')


@api_view(["POST"])
def start_scan(request, format=None):
    """
    调用开始扫描接口开始扫描
    :param request:
    :param format:
    :return:
    """
    attack_ids = request.data.get('attack_ids', [])
    if not attack_ids:
        return Response(success=False, data=[], message='attack_ids is empty')
    result = []
    for attack_id in attack_ids:
        success, data, message = scan(attack_id)
        result.append({'success': success, 'data': data, 'message': message})
    return Response(success=True, data=result, message="success")


@api_view(["GET"])
def fz_result(request, format=None):
    """
    获取fz的结果 列表详情使用
    :param request:
    :param format:
    :return:
    """
    source_ip = request.query_params.get("source_ip")
    data = {
        "scan_port": [],
        "web_server": [],
        "directory_blast": [],
        "vul": [],
        "weak_password": [],
    }
    if source_ip:
        data['scan_port'] = ScanPortSerializer(ScanPort.objects.filter(source_ip=source_ip), fields=["ports"],
                                               many=True).data

        data['web_server'] = WebServerSerializer(WebServer.objects.filter(source_ip=source_ip), fields=["site"],
                                                 many=True).data

        data['directory_blast'] = []
        dirbs = DirectoryBlast.objects.filter(source_ip=source_ip).values('raw_data')
        print(dirbs)
        for dir in dirbs:
            raw_data = dir['raw_data']
            site = f"{raw_data['service']}://{source_ip}:{raw_data['port']}"
            for d in raw_data['dirs']:
                data['directory_blast'].append(site + str(d[2]))
        data['vul'] = VulnerabilitySerializer(Vulnerability.objects.filter(source_ip=source_ip),
                                              fields=["name", "cve_num", "vul_site"],
                                              many=True).data
        data['weak_password'] = WeakPasswordSerializer(WeakPassword.objects.filter(source_ip=source_ip),
                                                       fields=["name", "cve_num", "vul_site"],
                                                       many=True).data
    return Response(success=True, data=data, message='success')

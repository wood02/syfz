import os
import time
from datetime import datetime, timedelta

from django_celery_beat.models import IntervalSchedule
from rest_framework.decorators import action
from rest_framework.views import APIView

from Syfz.settings import VERSION
from apps.system.models.global_conf import GlobalConfig
from apps.system.serializers.global_conf import GlobalConfigSerializer
from common.current.celery_task_util import SyfzTask
from common.drf.response import Response
from common.drf.viewsets import ModelViewSet, ListModelMixin, GenericViewSet, CreateModelMixin
from common.utils.check_port import check
from common.utils.ntp import get_ntp_time


class GlobalConfigViewSet(ListModelMixin, GenericViewSet):
    queryset = GlobalConfig.objects.all()
    serializer_class = GlobalConfigSerializer

    def verify_ports(self):
        ports = self.request.data.get("ports", "")
        port_list, err_list = check(ports)
        value = {"ports": port_list}
        return value, err_list

    def verify_sy_interval(self):
        interval = self.request.data.get("interval", 30)
        if not (interval and isinstance(interval, int)) and not (1 < interval < 60 * 24):
            return Response(success=False, data=[], message="数据格式错误！")

        value = {"interval": interval}
        return value, []

    def verify_status(self):
        status = self.request.data.get("status", 1)
        err_list = []
        if status not in [0, 1]:
            err_list.append(status)

        return status, err_list

    def verify_msg_relay_server(self):
        from common.utils.check_ip import is_ipv4
        err_list = []
        address = self.request.data.get("address", '')
        username = self.request.data.get("username", '')
        password = self.request.data.get("password", '')
        if not is_ipv4(address):
            err_list.append(address)
        value = {
            "address": address,
            "username": username,
            "password": password
        }

        return value, err_list

    def scan_conf(self, key_db, func, is_switch=False):
        if is_switch:
            fields = ["key", "name", "status"]
        else:
            fields = ["key", "name", "value"]
        if self.request.method == "GET":
            if key_db == "CONF_SCAN_SCHEME_":
                queryset = GlobalConfig.objects.filter(key__startswith=key_db)
                serializer = GlobalConfigSerializer(queryset, many=True, fields=fields + ["status"])
            else:
                if is_switch:
                    queryset = GlobalConfig.objects.filter(key=key_db)
                else:
                    queryset = GlobalConfig.objects.filter(key__startswith=key_db, status=1)
                serializer = GlobalConfigSerializer(queryset, many=True, fields=fields)
            data = serializer.data[0] if len(serializer.data) == 1 else serializer.data

            return Response(success=True, data=data, message="success")

        elif self.request.method == "POST":
            key = self.request.data.get("key", "")

            if not key and not key.startswith(key_db):
                return Response(success=False, data=None, message="参数错误！")

            value, err_list = func
            if err_list:
                return Response(success=False, data={"error": err_list}, message="数据格式有误")
            else:
                if not is_switch:
                    GlobalConfig.objects.filter(key=key).update(value=value)
                else:
                    GlobalConfig.objects.filter(key=key_db).update(status=value)

        return Response(success=True, data=None, message="success")

    @action(methods=['post'], detail=False, url_path='scan/scheme/checked', name="选中扫描方案")
    def scan_scheme_checked(self, request, *args, **kwargs):
        key = self.request.data.get("key", "")
        if not key:
            return Response(success=False, data=None, message="参数错误！")
        queryset = GlobalConfig.objects.filter(key__startswith="CONF_SCAN_SCHEME_")
        queryset.update(status=0)
        queryset.filter(key=key).update(status=1)
        return Response(success=True, data=None, message="success")

    @action(methods=['get', 'post'], detail=False, url_path='scan/scheme', name="扫描方案")
    def scan_scheme(self, request, *args, **kwargs):
        return self.scan_conf("CONF_SCAN_SCHEME_", self.verify_ports())

    @action(methods=['get', 'post'], detail=False, url_path='scan/auto_directory_blast', name="自动目录爆破")
    def auto_directory_blast(self, request, *args, **kwargs):
        return self.scan_conf("CONF_AUTO_DIRECTORY_BLAST", self.verify_ports())

    @action(methods=['get', 'post'], detail=False, url_path='scan/auto_weak_password_blast', name="自动弱口令爆破")
    def auto_weak_password_blast(self, request, *args, **kwargs):
        return self.scan_conf("CONF_AUTO_WEAK_PASSWORD_BLAST", self.verify_ports())

    @action(methods=['get', 'post'], detail=False, url_path='threat_intelligence/sy_interval', name="自动溯源间隔")
    def threat_intelligence(self, request, *args, **kwargs):
        # return self.scan_conf("THREAT_INTELLIGENCE_SY_INTERVAL", self.verify_sy_interval())

        if self.request.method == "GET":
            queryset = GlobalConfig.objects.filter(key__startswith="THREAT_INTELLIGENCE_SY_INTERVAL")
            serializer = GlobalConfigSerializer(queryset, many=True, fields=["key", "name", "value"])
            data = serializer.data[0] if len(serializer.data) == 1 else serializer.data

            return Response(success=True, data=data, message="success")

        elif self.request.method == "POST":
            key = self.request.data.get("key", "")
            if not key and not key.startswith(key):
                return Response(success=False, data=None, message="参数错误！")
            value, err_list = self.verify_sy_interval()
            if err_list:
                return Response(success=False, data={"error": err_list}, message="格式有误")
            else:
                GlobalConfig.objects.filter(key=key).update(value=value)
                st = SyfzTask(name="THREAT_INTELLIGENCE_SY_INTERVAL")
                st.update_or_create(value['interval'], "minutes", 'apps.system.tasks.tag_info_interval', )
                # start_time=datetime.now() + timedelta(seconds=10))

        return Response(success=True, data=None, message="success")

    @action(methods=['get', 'post'], detail=False, url_path='fz_conf/fz_model', name="反制模式")
    def fz_model(self, request, *args, **kwargs):
        return self.scan_conf("FZ_CONFIG_FZ_MODEL_SWITCH", self.verify_status(), is_switch=True)

    @action(methods=['get', 'post'], detail=False, url_path='fz_conf/msg_relay_server', name="消息中转服务器")
    def msg_relay_server(self, request, *args, **kwargs):
        return self.scan_conf("FZ_CONFIG_MSG_RELAY_SERVER", self.verify_msg_relay_server())

    # 常规
    @action(methods=['get', 'post'], detail=False, url_path='system_info', name="系统信息")
    def system_info(self, request, *args, **kwargs):
        # ntps = get_ntp_time()
        ntps = []
        if ntps:
            ntp_time = ntps[0]['ntp_time']
            local_time = ntps[0]['local_time']
        else:
            ntp_time = []
            localtime = datetime.now()
            local_time_str = localtime.strftime('%Y-%m-%d %H:%M:%S')

        result_time = {
            "ntp_time": ntp_time,
            "local_time": [time.mktime(localtime.timetuple()), local_time_str],
        }
        queryset = GlobalConfig.objects.filter(key="SYSTEM_INFO", status=1)
        serializer = GlobalConfigSerializer(queryset, many=True, fields=["value"])
        result = {
            # todo: 可以改成获取系统信息的方法
            # "system_name": "溯源反制自动化系统",

        }
        if serializer.data:
            result.update(serializer.data[0].get("value", {}))
        result.update(result_time)
        return Response(success=True, data=result)


class SystemTimeApiView(APIView):

    def get(self, request):
        ntps = get_ntp_time()

        if ntps:
            ntp_time = ntps[0]['ntp_time']
            local_time = ntps[0]['local_time']
        else:
            ntp_time = []
            localtime = datetime.now()
            local_time = localtime.strftime('%Y-%m-%d %H:%M:%S')

        result = {
            "ntp_time": ntp_time,
            "local_time": local_time,
        }
        return Response(success=True, data=result)

    def post(self, request):
        try:
            # os.system("sh /code/chrony.sh service")
            # with open("chrony.sh") as f:
            #     content = f.read()
            return Response(success=True, data=[])
        except Exception:
            return Response(success=False, message="校时失败！", data=[])

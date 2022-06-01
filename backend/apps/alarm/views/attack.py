# -*- coding: utf-8 -*-
import datetime
import os.path

from django.db import transaction
from django.db.models import Count
from django.http import FileResponse, StreamingHttpResponse
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from Syfz.settings import BASE_DIR
from apps.alarm.filters.attack_filters import AttackFilter, AttackFilterBackend, AttackWhiteFilter
from apps.alarm.models import Attack, AttackDetails, AttackWhite
from apps.alarm.serializers.attack_ser import AttackSerializer, BatchAttackSerializer, AttackDetailsSerializer, \
    AttackUpdateSerializer, AttackListSerializer, AttackWhiteSerializer
from common.drf.response import Response
from common.drf.viewsets import ModelViewSet
from common.utils.check_ip import is_ipv4, check_ipv4_segment
from common.utils.fileupload import FileUpload


class AttackViewSet(ModelViewSet):
    queryset = Attack.objects.all()
    serializer_class = AttackSerializer
    filter_backends = [AttackFilterBackend]
    filter_class = AttackFilter

    def get_queryset(self):
        queryset = self.queryset
        order = self.request.query_params.get("order")

        if self.action in ["list"] and order in [
            'attack_earliest_time', "-attack_earliest_time",
            'trace_rate', '-trace_rate',
            'domain_num', '-domain_num',
        ]:
            queryset = queryset.order_by(order)
        return queryset

    def get_serializer_class(self):
        if self.action in ["batch_create"]:
            return BatchAttackSerializer
        if self.action in ["update"]:
            return AttackUpdateSerializer
        if self.action in ['list']:
            return AttackListSerializer
        else:
            return AttackListSerializer

    @action(methods=['post'], detail=False, url_path='batch_create', name="批量新增")
    def batch_create(self, request, *args, **kwargs):
        err_data = {"exists_ips": [], "white_ips": [], "err_ips": []}
        ips = self.request.data.get("ips")
        if not ips:
            return Response(success=False, message="参数错误！")
        else:
            ips = ips.strip().split("\n")
        if len(ips) >= 50:
            return Response(success=False, message="不得大于50个")
        queryset = Attack.objects.filter(source_ip__in=ips).values("source_ip")

        if queryset:
            err_data["exists_ips"] = [i['source_ip'] for i in queryset]
            return Response(success=False, data=err_data, message="批量新增失败！")

        not_ipv4 = []
        exists_ips = []
        white_ips = []
        created_ips = []
        for source_ip in ips:
            if not is_ipv4(source_ip):
                not_ipv4.append(source_ip)
            aw_query = AttackWhite.objects.filter(white_ip=source_ip)
            if aw_query:
                white_ips.append(source_ip)
        if not_ipv4 or white_ips:
            err_data["err_ips"] = not_ipv4
            err_data["white_ips"] = white_ips
            return Response(success=False, data=err_data, message="批量新增失败！")
        for source_ip in ips:
            attack_query, created = Attack.objects.get_or_create(source_ip=source_ip,
                                                                 attack_earliest_time=datetime.datetime.now())
            if not created:
                exists_ips.append(source_ip)
            else:
                # todo 自动任务
                from apps.alarm.conf import TASK_ADD
                if created and TASK_ADD:
                    # todo 后台任务
                    from apps.alarm.tasks import run_alarm_detail
                    run_alarm_detail(source_ip, attack_query.id)

                created_ips.append(source_ip)
        return Response(success=True, data=[{"exits_ips": exists_ips, "created_ips": created_ips}], message="批量新增成功！")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        AttackWhite.objects.get_or_create(white_ip=instance.source_ip)
        return Response(code=200, success=True, message="删除成功，并加入白名单！")

    @action(methods=['delete'], detail=False, url_path='batch_del', name="批量删除加白")
    def batch_del(self, request, *args, **kwargs):
        ids = self.request.data.get("ids", [])
        if not ids:
            return Response(success=False, message="参数错误！")
        queryset = Attack.objects.filter(id__in=ids)
        for q in queryset:
            AttackWhite.objects.get_or_create(white_ip=q.source_ip)
        queryset.delete()

        return Response(code=200, success=True, message="删除成功，并加入白名单！")

    @action(methods=['get'], detail=False, url_path='down_template', name="下载模板")
    def down_template(self, request, *args, **kwargs):
        try:
            file_path = os.path.join(BASE_DIR, 'data/files/template/template_sygl.xlsx')
            # response_file = FileResponse(open(file_path, 'rb'))
            # response_file['content_type'] = "application/octet-stream"
            # response_file['Content-Disposition'] = 'attachment; filename=template.xlsx'
            # + os.path.basename(file_path)

            response_file = StreamingHttpResponse(open(file_path, 'rb'))  # 以二进制形式响应数据流

            response_file['Content-Type'] = 'application/octet-stream'  # 浏览器不识别的也会自动下载
            response_file['Content-Disposition'] = 'attachment; filename=template.xlsx'
            return response_file
        except FileNotFoundError:
            return Response(success=False, message="模板文件不存在！")

    @action(methods=['post'], detail=False, url_path='upload', name="导入文件")
    def upload(self, request, *args, **kwargs):

        file_obj = request.FILES.get('file')  # 前台读取到 name='file'
        fu = FileUpload(f_obj=file_obj, ext=['xlsx', 'xls', 'csv'], size=1024 * 1024 * 5)
        b, f = fu.load()
        if not b:
            return Response(success=False, message=f)
        result = read_excel(f_obj=file_obj)
        return result


def read_excel(f_obj):
    import pandas as pd

    # 读取Excel数据
    from apps.alarm.models import Attack, AttackWhite
    from apps.alarm.serializers.attack_ser import AttackSerializer, AttackDetailsSerializer
    from common.utils.check_ip import is_ipv4

    df = pd.read_excel(f_obj, sheet_name=0, usecols=[0, 1, 2, 3, 4])
    columns = df.columns.values.tolist()
    if columns != ['源IP', '攻击时间', '目的IP', '攻击手法', '来源']:
        return Response(success=True, data=[], message="文件格式错误！")

    df = df.where(df.notnull(), "")
    err_data = {"exists_ips": [], "white_ips": [], "err_ips": [], "error_details": []}

    not_ipv4 = []
    white_ips = []
    error_details = []
    ips_list = []
    for idx, row in df.iterrows():
        ips_dict = {}
        source_ip = row[0]

        ips_dict['source_ip'] = row[0]
        attack_detail = {
            "attack_time": row[1],
            "destination_ip": row[2],
            "attack_type": row[3],
            "source": row[4]
        }

        ips_dict['index'] = idx + 2
        ips_dict['attack_detail'] = attack_detail
        append_date = {'row': idx + 2, 'source_ip': source_ip}
        if not is_ipv4(source_ip):
            not_ipv4.append(append_date)
        aw_query = AttackWhite.objects.filter(white_ip=source_ip)
        if aw_query:
            white_ips.append(append_date)
        ad_ser = AttackDetailsSerializer(data=attack_detail)
        if not ad_ser.is_valid():
            append_date['errors'] = ad_ser.errors
            error_details.append(append_date)
        ips_list.append(ips_dict)
    queryset = Attack.objects.filter(source_ip__in=[i['source_ip'] for i in ips_list]).values("source_ip")

    # if queryset:
    #     err_data['exists_ips'] = [i['source_ip'] for i in queryset]
    #     return Response(success=False, data=err_data, message="数据导入失败！")
    if not_ipv4 or white_ips or error_details:
        err_data['err_ips'] = not_ipv4
        err_data['white_ips'] = white_ips
        err_data['error_details'] = error_details

        return Response(success=False, data=err_data, message="数据导入错误！")
    exists_ips = []
    created_ips = []

    try:
        with transaction.atomic():
            # 不建议使用事务处理
            for ips in ips_list:
                source_ip = ips['source_ip']
                attack_detail = ips['attack_detail']
                row = ips['index']
                append_date = {'row': row, 'source_ip': source_ip}
                ser_data = {
                    'source_ip': source_ip,
                    "attack_details": [
                        attack_detail
                    ]
                }

                # 这部分代码会在事务中执行
                # 创建回滚点
                save_id = transaction.savepoint()

                attack_query, created = Attack.objects.get_or_create(source_ip=source_ip)
                if not created:
                    exists_ips.append(append_date)
                else:
                    #  1.创建详细 2.自动任务

                    created_ips.append(append_date)
                serializer = AttackSerializer(data=ser_data)
                if serializer.is_valid():
                    serializer.save()

                else:
                    print(serializer.errors)
                    # 一旦异常，则回滚代码 双层保障
                    raise Exception("数据错误")
    except Exception as e:
        print(e)
        transaction.savepoint_rollback(save_id)
    data = [{"exits_ips": exists_ips, "created_ips": created_ips}]
    return Response(success=True, data=data, message="数据导入成功！")


class AttackDetailsViewSet(GenericViewSet):
    queryset = AttackDetails.objects.all()
    serializer_class = AttackDetailsSerializer

    @action(methods=['get'], detail=False, url_path='get/attack_types', name="获得攻击类型")
    def attack_type(self, request, *args, **kwargs):
        queryset = AttackDetails.objects.all()
        attack_details = queryset.values('attack_type').annotate(count=Count('id')).order_by('attack_type')
        return Response(success=True, data=list(attack_details), message="获得成功！")


class AttackWhiteViewSet(ModelViewSet):
    queryset = AttackWhite.objects.all()
    serializer_class = AttackWhiteSerializer
    filter_class = AttackWhiteFilter

    def create(self, request, *args, **kwargs):
        ips = self.request.data.get("ips")
        remark = self.request.data.get("remark")

        if not ips:
            return Response(success=False, message="参数错误！")
        else:
            ips = ips.strip().split("\n")
        white_ips = []
        aw_ips = []
        not_meet = []
        exists_ips = []
        for ip in ips:
            v4_segment = check_ipv4_segment(ip)
            if not v4_segment:
                not_meet.append(ip)
            aw = AttackWhite.objects.filter(white_ip=ip)
            if aw:
                exists_ips.append(ip)
            else:
                white_ips.append(ip)
                aw_ips.append(AttackWhite(white_ip=ip, remark=remark))
        if not_meet:
            return Response(success=False, data=[{"error_ips": not_meet}], message="批量新增失败！")
        AttackWhite.objects.bulk_create(aw_ips)
        return Response(success=True, data=[{"exits_ips": exists_ips, "created_ips": white_ips}], message="批量新增成功！")

    @action(methods=['DELETE'], detail=False, url_path='batch_del', name="批量删除")
    def batch_del(self, request, *args, **kwargs):
        ids = self.request.data.get("ids")
        if not ids or not isinstance(ids, list):
            return Response(success=False, message="参数错误！")
        else:
            AttackWhite.objects.filter(id__in=ids).delete()  # 用id__in 来拿取数据 紧接着删除
            return Response(success=True, message="删除成功！")

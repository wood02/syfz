import os
import platform
import sys
from datetime import datetime
from subprocess import run

from django.http import HttpResponse, FileResponse, JsonResponse
from django.utils.encoding import escape_uri_path
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters, permissions
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.viewsets import ModelViewSet

from rest_framework.decorators import action

from Syfz.settings import BASE_DIR
from apps.poc.filter import PocFilter
from apps.poc.models import Poc
from apps.poc.serializer import PocSerializer, PocListSerializer


def make_response(data=None, message='success', code=200):
    resp = dict()
    resp['message'] = message
    resp['code'] = code
    resp['success'] = True if code == 200 else False
    resp['data'] = data
    return resp


class PocViewSet(ModelViewSet):
    queryset = Poc.objects.all().order_by('-id')
    serializer_class = PocSerializer

    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # 添加权限

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = PocFilter  # 过滤类
    # filter_fields = ('poc_name', 'vulnerability', 'insert_tm', 'user')
    # search_fields = ('id', 'poc_name', 'vulnerability', 'insert_tm', 'user_id', 'user_username')
    # # 排序
    ordering_fields = ('created_at', 'id')

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return PocListSerializer
        else:
            return PocSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.user.id
        request.data['user'] = user_id
        serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        if not serializer.is_valid():
            return JsonResponse(make_response([], serializer.errors.get('msg'), 101))
        self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        return JsonResponse(make_response(data=serializer.data), status=HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='download', name="下载PoC编写指南")
    def download(self, request, *args, **kwargs):
        file_name = 'Poc编写指南.docx'
        path = os.path.join(BASE_DIR, 'data/files/pocs/' + file_name)
        # print(path)
        file = open(path, 'rb')
        # response = HttpResponse(file, content_type="application/octet-stream")
        # response["Access-Control-Expose-Headers"] = "Content-Disposition"  # 为了使前端获取到Content-Disposition属性
        # response['Content-Disposition'] = 'attachment;filename={0}'.format(file_name)
        response = FileResponse(file, filename=file_name)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = "attachment;filename*=utf-8''{}".format(escape_uri_path(file_name))
        response["Access-Control-Expose-Headers"] = "Content-Disposition"  # 为了使前端获取到Content-Disposition属性
        return response

    @action(methods=['post'], detail=False, url_path='upload', name="批量新增")
    def upload(self, request, *args, **kwargs):
        files = request.FILES.getlist('files')
        for file in files:
            path = "data/files/pocs/" + file.name

            if os.path.exists(os.path.join(BASE_DIR, path)):
                path = path.split('.')[-2] + '_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.' + \
                       file.name.split('.')[-1]
            with open(os.path.join(BASE_DIR, path), 'wb') as f:
                for i in file.chunks():
                    f.write(i)
            # 上传到docker-hack容器中
            # p_sys = platform.system()
            # if p_sys == "Linux":
            #     cmd = f'docker cp {path} hack:/home/tools/pocjson/pocs'
            #     run(cmd, shell=True)

        return JsonResponse(make_response())

    # 过滤和分页
    def list(self, request, *args, **kwargs):
        # 过滤
        queryset = self.filter_queryset(self.get_queryset())
        # 分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse(make_response(),
                            status=status.HTTP_200_OK)

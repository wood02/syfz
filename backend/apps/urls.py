# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.urls import path
from django.contrib.staticfiles.views import serve
from rest_framework.permissions import AllowAny

from django.urls import re_path
from django.contrib.staticfiles.views import serve

app_name = 'api'


def return_static(request, path, insecure=True, **kwargs):
    """
    https://www.cnblogs.com/hd92/p/15875369.html
    :param request:
    :param path:
    :param insecure:
    :param kwargs:
    :return:
    """
    return serve(request, path, insecure, **kwargs)


urlpatterns = [
    # url(r'alarm/', include('apps.alarm.urls', namespace='alarm')),
    url(r'api/', include('apps.alarm.urls'), name='alarm'),
    url(r'', include('apps.user.urls'), name='user'),
    url(r'api/', include('apps.system.urls'), name='system'),
    url(r'api/', include('apps.tracesource.urls'), name='tracesource'),
    url(r'api/', include('apps.plugins.urls'), name='plugins'),
    url(r'api/', include('apps.poc.urls'), name='poc'),


    path('api/', include('rest_framework.urls')),  # drf管理
    re_path(r'^static/(?P<path>.*)$', return_static, name='static'),  # 添加这行 uwsgi启动需要加static-map


]
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# API文档
schema_view = get_schema_view(
    openapi.Info(title="SYFZ API", default_version="v1", description="溯源反制"),
    public=True,
    permission_classes=(AllowAny,),

)()

# API文档
urlpatterns += [
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    re_path(r"^swagger/$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    re_path(r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

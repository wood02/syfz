# -*- coding: utf-8 -*-
from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.tracesource.views import fz_view
from apps.tracesource.views import ts_conf

router = DefaultRouter()
routers = {
    'tracesource/scan_port': fz_view.ScanPortViewSet,
    'tracesource/web_server': fz_view.WebServerViewSet,
    'tracesource/dir_blast': fz_view.DirectoryBlastViewSet,
    'tracesource/vul': fz_view.VulnerabilityViewSet,
    'tracesource/weak_psw': fz_view.WeakPasswordViewSet,
    'tracesource/ts_server': ts_conf.TsServerViewSet,

}
for key, value in routers.items():
    router.register(key, value)
urlpatterns = [
    path('tracesource/fz_result/', fz_view.fz_result, name='fz_result'),
    # path('tracesource/callback/', fz_view.callback, name='callback'),
    path('tracesource/start_scan/', fz_view.start_scan, name='start_scan'),
]
urlpatterns += router.urls

# -*- coding: utf-8 -*-
from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.system.views import global_conf,audit_log
from apps.system.views.global_conf import SystemTimeApiView

router = DefaultRouter()
routers = {
    'system/config': global_conf.GlobalConfigViewSet,
    'system/audit_log/login': audit_log.LoginEventViewSet,
    'system/audit_log/operation': audit_log.OperationLogViewSet,

}

for key, value in routers.items():
    router.register(key, value)
urlpatterns = [
    # path('detail_fofa/', attack_detail.DetailFofaAPIView.as_view(), name='fofa'),
    path('ntp/', SystemTimeApiView.as_view(), name="system_ntp"),

]
urlpatterns += router.urls

# -*- coding: utf-8 -*-
from apps.system.filters.audit_log import LoginEventFilter, OperationLogFilter
from apps.system.models import LoginEvent, OperationLog
from apps.system.serializers.audit_log import LoginEventSerializer, OperationLogSerializer
from common.drf.viewsets import ModelViewSet, RetrieveModelMixin, ListModelMixin, GenericViewSet


class LoginEventViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = LoginEvent.objects.all()
    serializer_class = LoginEventSerializer
    filter_class = LoginEventFilter
    # permission_classes = []


class OperationLogViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = OperationLog.objects.all()
    serializer_class = OperationLogSerializer
    filter_class = OperationLogFilter

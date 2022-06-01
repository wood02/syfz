# -*- coding: utf-8 -*-
from apps.tracesource.models import TsServer
from apps.tracesource.serializers.ts_conf import TsServerSerializer
from common.drf.viewsets import ModelViewSet


class TsServerViewSet(ModelViewSet):
    queryset = TsServer.objects.all()
    serializer_class = TsServerSerializer
    # filter_class = TsServerFilter

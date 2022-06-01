# -*- coding: utf-8 -*-
from apps.alarm.models import FofaToken, XtbApiKey, NsfocusApiKey, ZoomEyeToken
from apps.alarm.serializers.passive_ser import FofaTokenSerializer, XtbApiKeySerializer, NsfocusApiKeySerializer, \
    ZoomEyeTokenSerializer
from common.drf.viewsets import ModelViewSet


class FofaTokenViewSet(ModelViewSet):
    queryset = FofaToken.objects.all()
    serializer_class = FofaTokenSerializer


class XtbApiKeyViewSet(ModelViewSet):
    queryset = XtbApiKey.objects.all()
    serializer_class = XtbApiKeySerializer


class NsfocusApiKeyViewSet(ModelViewSet):
    queryset = NsfocusApiKey.objects.all()
    serializer_class = NsfocusApiKeySerializer


class ZeyeTokenViewSet(ModelViewSet):
    queryset = ZoomEyeToken.objects.all()
    serializer_class = ZoomEyeTokenSerializer

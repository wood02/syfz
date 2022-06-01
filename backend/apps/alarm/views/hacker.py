# -*- coding: utf-8 -*-
from django_filters.rest_framework import DjangoFilterBackend

from apps.alarm.filters.hacker_filter import HackerFilter
from apps.alarm.models import Hacker, EvidenceImage
from apps.alarm.serializers.hacker_ser import HackerListSerializer, HackerCreateUpdateSerializer, \
    EvidenceImageSerializer, HackerSimpleListSerializer
from common.drf.viewsets import ModelViewSet


class HackerViewSet(ModelViewSet):
    queryset = Hacker.objects.all()
    filter_class = HackerFilter

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return HackerCreateUpdateSerializer
        elif self.action in ['list']:
            return HackerSimpleListSerializer
        else:
            return HackerListSerializer


class EvidenceImageViewSet(ModelViewSet):
    queryset = EvidenceImage.objects.all()
    serializer_class = EvidenceImageSerializer

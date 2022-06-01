# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import json

from rest_framework.decorators import action

from apps.alarm.filters.event_filter import EventFilter
from apps.alarm.models import Event, EventFile
from apps.alarm.serializers.event_ser import EventFileSerializer, EventCreateUpdateSerializer, EventListSerializer
from common.drf.viewsets import ModelViewSet


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    filter_class = EventFilter

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return EventCreateUpdateSerializer
        else:
            return EventListSerializer


class EventFileViewSet(ModelViewSet):
    queryset = EventFile.objects.all()
    serializer_class = EventFileSerializer

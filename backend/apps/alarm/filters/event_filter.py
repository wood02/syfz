import django_filters

from apps.alarm.models import Hacker, Event


class EventFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Event

        fields = ["title"]


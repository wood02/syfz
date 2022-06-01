import django_filters

from apps.alarm.models import Hacker


class HackerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Hacker
        fields = ["name", "age"]
        # fields = {
        #     "name": ['exact', 'icontains'],
        #     "age": ['exact', 'gte', 'lte'],
        # }

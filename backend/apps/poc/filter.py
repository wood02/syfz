from django_filters import rest_framework as filters

from apps.poc.models import Poc


class PocFilter(filters.FilterSet):
    start_time = filters.DateTimeFilter(field_name="created_at", lookup_expr='gte')
    end_time = filters.DateTimeFilter(field_name="created_at", lookup_expr='lte')
    poc_name = filters.CharFilter(field_name="poc_name", lookup_expr="icontains")
    vulnerability = filters.CharFilter(field_name="vulnerability", lookup_expr="icontains")

    username = filters.CharFilter(field_name="user_id__username", lookup_expr="icontains")

    class Meta:
        model = Poc  # 模型名
        fields = ['id']

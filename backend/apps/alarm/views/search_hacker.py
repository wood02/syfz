# -*- coding: utf-8 -*-
from drf_haystack.filters import HaystackHighlightFilter
from drf_haystack.generics import HaystackGenericAPIView
from drf_haystack.viewsets import HaystackViewSet
from haystack.query import SearchQuerySet
from haystack.utils import Highlighter

from apps.alarm.models import Hacker
from apps.alarm.serializers.search_hacker_ser import HackerIndexSerializer


class HackerSearchViewSet(HaystackViewSet):
    index_models = [Hacker]
    serializer_class = HackerIndexSerializer
    # filter_backends = [HaystackHighlightFilter]  # Whoosh不支持 支持es solr
    # 存python 高亮 让它支持Whoosh
    highlighter_class = Highlighter
    highlighter_css_class = "highlighted"
    highlighter_html_tag = "em"
    highlighter_max_length = 200
    highlighter_field = None

    def filter_queryset(self, queryset):
        queryset = super(HaystackGenericAPIView, self).filter_queryset(queryset)

        if self.load_all:
            queryset = queryset.load_all()

        return queryset.order_by("-id")

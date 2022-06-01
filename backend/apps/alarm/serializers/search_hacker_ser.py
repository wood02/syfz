# -*- coding: utf-8 -*-
from drf_haystack.serializers import HighlighterMixin, HaystackSerializer

from apps.alarm.search_indexes import HackerIndex
from apps.alarm.serializers.hacker_ser import HackerListSerializer


class HackerIndexSerializer(HighlighterMixin, HaystackSerializer):
    object = HackerListSerializer(read_only=True)  # 只读,不可以进行反序列化
    highlighter_css_class = "highlighter-class"
    highlighter_html_tag = "em"

    class Meta:
        index_classes = [HackerIndex]  # 索引类的名称
        fields = ['q', 'object', 'address', 'name']  # q 由索引类进行返回, object 由序列化类进行返回,第一个参数必须是text
        field_aliases = {
            # 别名,又名
            "kw": "q"
        }

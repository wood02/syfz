#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict


class MyPageNumberPagination(PageNumberPagination):
    """
    修改默认分页配置
    """
    page_size = 10  # 每页显示多少条
    page_size_query_param = 'page_size'  # URL中每页显示条数的参数
    page_query_param = 'page'  # URL中页码的参数
    max_page_size = 250  # 每页最多显示个数

    def get_paginated_response(self, data, *args, **kwargs):
        result = [
            ('count', self.page.paginator.count),
            # ('current_page ', self.page.number),
            # ('total_page ', self.page.paginator.num_pages),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]
        for key, value in kwargs.items():
            result.append((key, value))
        return Response(OrderedDict(result))

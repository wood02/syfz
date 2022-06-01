from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from common.utils.customize import make_response


class StandardResultsSetPagination(PageNumberPagination):
    """全局的分页类，所有的list请求会调用"""

    page_size = 10  # 每页显示的条数
    page_size_query_param = 'page_size'  # 前端发送的页数关键字名
    max_page_size = 20  # 每页最大显示的条数

    def get_paginated_response(self, data):
        # Response(make_response(data))
        return Response(make_response(data))


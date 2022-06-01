#!/usr/bin/env python
# encoding:utf-8
from asgiref.sync import sync_to_async
from loguru import logger

from apps.alarm.utils.fofa import FofaClient
from apps.alarm.utils.zeye import ZeyeClient


def get_data(query, page=1):
    if page < 1:
        page = 1

    client = ZeyeClient()
    # +ip: "156.240.109.234" + port:"80" + after: "2021-01-25 16:37:59"
    raw_data = client.get(query_str=query, page=page)

    titles = {
        'sit': '站点',
        'title': '标题',
        'timestamp': '发现时间',
        'organization': '组织',

    }
    return titles, raw_data


async def search(query, page=1):
    logger.info(f"[Fofa资产测绘] APP 执行参数为: query:{query},page:{page}")

    titles, raw_data = await sync_to_async(get_data)(query=query, page=page)
    return {"status": 0, "result": {"titles": titles, "data": raw_data}}

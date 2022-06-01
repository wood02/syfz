#!/usr/bin/env python
# encoding:utf-8
from asgiref.sync import sync_to_async
from loguru import logger

from apps.alarm.utils.threatbook import xbt_conf
from apps.alarm.utils.threatbook.xtb_mul import ThreatBookMul
from apps.system.models import GlobalConfig
from common.utils import check_ip


def get_data(query):
    mul_data = [{"ip": query}]

    if check_ip.check_ip(query):
        # url = "https://api.threatbook.cn/v3/ip/query"
        url = xbt_conf.conf("ip_query")
    else:
        url = xbt_conf.conf("domain_query")
        # url = "https://api.threatbook.cn/v3/domain/query"  # 测试域名
    tb = ThreatBookMul(mul_data=mul_data, url=url, is_mul=False, is_adv=False)
    data, success = tb.parse(save_to=None)
    return data, success


async def search(query):
    logger.info("[ThreatBook] APP 执行参数为: {query}", query=query)
    data, success = await sync_to_async(get_data)(query=query)
    mul_data = [{"ip": query}]
    if success:
        data = data['data'][mul_data[0]['ip']]
        return {"status": 0, "result": {"titles": {}, "data": data}}
    else:
        return {"status": 2, "result": {"titles": {}, "data": data}}

#!/usr/bin/env python
# encoding:utf-8
from asgiref.sync import sync_to_async
from loguru import logger


def get_data():
    from apps.system.models import GlobalConfig

    v = GlobalConfig.objects.filter(key="TOOLSET_THIRD_PARTY_SITE").first().value
    data = v['GenSocialWorkerPsw']
    data["args"]["url"] = data["args"]["url"].format(ip=v['base']['ip'])

    return data


async def get_site():
    logger.info("[GenSocialWorkerPsw] APP 执行参数为:")
    data = await sync_to_async(get_data)()
    return {"status": 0, "result": data}

#!/usr/bin/env python
# encoding:utf-8
import requests
from loguru import logger


async def weather(city):
    logger.info("[查询天气-百度接口] APP 执行参数为: {city}", city=city)
    url = f"https://www.baidu.com/home/other/data/weatherInfo?city={city}"
    response = requests.get(url=url)

    return {"status": 0, "result": {"key": "baidu", "data": response.json()}}

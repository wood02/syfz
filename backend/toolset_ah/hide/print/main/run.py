#!/usr/bin/env python
# encoding:utf-8
from loguru import logger


async def print_content(content):
    logger.info("[Print] APP 执行参数为: {content}", content=content)
    return {"status": 0, "result": content}

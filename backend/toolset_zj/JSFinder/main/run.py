#!/usr/bin/env python
# encoding:utf-8
import os

from loguru import logger

from toolset.JSFinder.main.JSFinderPlus.JSFinderPlus import run


async def search(url):
    logger.info("[JSFinderPlus] APP 执行参数为: {url}", url=url)

    data = run(url=url)
    # cmd = "cd toolset/JSFinder/main/JSFinderPlus &&  python ./JSFinderPlus.py  -d -u {url}".format(url=url)
    # logger.info("[JSFinderPlus] APP 执行命令为: {cmd}", cmd=cmd)
    # os.system(cmd)
    titles = {
        "id": "ID",
        "url": "url",
        "info": "状态/信息",
        "time": "创建时间",
    }
    result = {"titles": titles, "data": data}
    return {"status": 0, "result": result}

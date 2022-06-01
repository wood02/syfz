#!/usr/bin/env python
# encoding:utf-8
from asgiref.sync import sync_to_async
from loguru import logger

from apps.alarm.utils.location import IpWW


def get_data(ips):
    ips = ips.split("\n")
    raw_data = []
    data = []
    for ip in ips:
        iww = IpWW(ip, is_save=False)
        d = iww.get()

        if d:
            m = d['multiAreas']
            data.append({
                "ip": ip,
                "lat": m['lat'],
                "lng": m['lng'],
                "radius": m['radius'],
                "address": m['prov'] + m['city'] + m['district'],
                "handle": f"<a href='https://www.amap.com/regeo?lng={m['lng']}&lat={m['lat']}' class='amap' target='_blank'>地图取点</a>",
            })
        raw_data.append(d)

    titles = {
        "ip": "IP",
        'address': '地理位置',
        'radius': '覆盖半径',
        'lat': '纬度',
        'lng': '经度',
        'handle': '操作',
    }
    return titles, data, raw_data


async def search(ips):
    logger.info(f"[精确地理位置查询] APP 执行参数为: ips: {ips}")
    titles, data, raw_data = await sync_to_async(get_data)(ips)
    return {"status": 0, "result": {"titles": titles, "data": data, "raw_data": raw_data}}

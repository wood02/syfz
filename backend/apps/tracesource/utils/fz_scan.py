# -*- coding: utf-8 -*-
import datetime

from urllib3.exceptions import ReadTimeoutError

from Syfz.setup import *
import json

import requests
from requests import ReadTimeout

from apps.alarm.models import Attack
from apps.system.models import GlobalConfig
from apps.tracesource.utils.parse_data import parse
from common.current.log import get_logger

get_logger = get_logger("celery", 'celery_beat.log',
                        filter=lambda record: "celery_beat" in record["extra"])
logger = get_logger.bind(celery_beat=True)


def scan(attack_id):
    g = GlobalConfig.objects.filter(key="TS_SCAN_CONF").first()
    success = False
    message = "success"
    data = []
    attack = Attack.objects.filter(id=attack_id).first()
    if g:
        v = g.value
        method = v['scan']['method']
        url = v['scan']['url']

        if attack:
            # todo: 判断是否已经扫描过 需要改成 !=0
            # if attack.fz_status != 0:
            #     message = "已反制"
            #     data = {"task_id": attack.fz_task_id}
            # else:
            queryset = GlobalConfig.objects.filter(key__startswith="CONF_SCAN_SCHEME_", status=1).first()
            ports = queryset.value.get("ports")
            ports = ",".join([str(p) for p in ports])
            rd = {"ip": attack.source_ip, "ports": ports, "task_id": attack.fz_task_id}
            try:
                response = requests.request(method, url, data=rd, timeout=3)
                rj = response.json()
                if rj['code'] == 200:
                    success = True
                    data = rj['data']
                    data['source_ip'] = attack.source_ip
                    data['port'] = ports
                    attack.fz_task_id = data['task_id']
                    attack.fz_status = 1
                    attack.fz_start_time = datetime.datetime.now()
                    attack.save()
                else:
                    message = rj.get('message', "下发任务失败")
            except ReadTimeout as e:
                message = "下发任务超时，请联系管理员"
                logger.error(str(e))
                data = {"source_ip": attack.source_ip}
            except Exception as e:
                message = "下发任务失败，请联系管理员"
                logger.error(str(e))

        else:
            message = "数据错误，请联系管理员"
    else:
        message = "配置错误，请联系管理员"
    logger.warning(f"成功与否：{success}  数据：{data}  信息：{message}")
    if not success:
        data = {"source_ip": attack.source_ip if attack else ""}
    return success, data, message


def scan_result(task_ids):
    g = GlobalConfig.objects.filter(key="TS_SCAN_CONF").first()

    if g:
        v = g.value
        url = v['scan_result']['url']

        payload = json.dumps({
            "task_ids": task_ids
        })
        headers = {
            'Content-Type': 'application/json'
        }
        try:
            response = requests.request("POST", url, headers=headers, timeout=3, data=payload)
            rj = response.json()
            if rj['code'] == 200:
                for t in rj['data']:
                    if t['successful']:
                        Attack.objects.filter(fz_task_id=t['task_id']).update(fz_status=2,
                                                                              fz_end_time=datetime.datetime.now(),
                                                                              fz_result_raw=t)
                        parse(t['result'])
        except Exception as e:
            logger.error(f"扫描异常: {str(e)}")


if __name__ == '__main__':
    scan_result([
        "1754afc4-4e76-44c2-be2f-5b1988a2f4c6"
    ])

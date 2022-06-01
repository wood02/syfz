# -*- coding: utf-8 -*-
import time

from celery import shared_task
from tenacity import RetryError

from apps.alarm.models import Attack
from apps.alarm.utils.threatbook import xbt_conf
from apps.tracesource.tasks import run_scan
from apps.system.models import GlobalConfig
from common.current.log import get_logger

get_logger = get_logger("celery", 'celery_worker.log',
                        filter=lambda record: "celery_worker" in record["extra"])
logger = get_logger.bind(celery_worker=True)


@shared_task(bind=True, default_retry_delay=10)
def add(self):
    try:
        time.sleep(30)
        raise Exception()
    except Exception as exc:
        # overrides the default delay to retry after 1 minute
        logger.warning(self.request)
        logger.warning(self.request.retries)
        # self.request.retries = 3
        logger.warning("异常重试")
        raise self.retry(exc=exc, countdown=6, max_retries=3)


@shared_task(bind=True)
def ip2domain(self, ip, parent_id):
    """
    retry的参数可以有：
        exc：指定抛出的异常
        throw：重试时是否通知worker是重试任务
        eta：指定重试的时间／日期
        countdown：在多久之后重试（每多少秒重试一次）
        max_retries：最大重试次数
    """
    try:
        from apps.alarm.utils.ip2domain import IP2Domain
        itod = IP2Domain(ip, parent_id)
        return itod.searchDomain()
    except Exception as exc:
        # logger.warning(self.request.retries)
        logger.warning("IP查域名异常异常重试")
        raise self.retry(exc=exc, countdown=5, max_retries=2)


@shared_task(bind=True)
def location(self, ip, parent_id):
    try:
        from apps.alarm.utils.location import IpWW
        ww = IpWW(ip, parent_id)
        return ww.get()
    except Exception as exc:
        # logger.warning(self.request.retries)
        logger.warning("地理位置异常重试")
        raise self.retry(exc=exc, countdown=5, max_retries=3)


@shared_task
def nsfocus(ip, parent_id):
    from apps.alarm.utils.nsfocus import NsfocusCilent
    tb = NsfocusCilent(ip, parent_id)
    return tb.get()


@shared_task
def asset_num(ip, parent_id):
    from apps.alarm.utils.fofa import FofaClient
    fo = FofaClient()
    return fo.get_asset_num(ip, parent_id)


@shared_task(bind=True)
def ip_query(self, ip, parent_id):
    """
    扫描微步的IP分析 主要包含端口
    :return:
    """
    try:
        from apps.alarm.utils.threatbook.xtb_mul import ThreatBookMul
        mul_data = [{"ip": ip, "parent_id": parent_id}]
        url = xbt_conf.conf("ip_query")
        # url = "https://api.threatbook.cn/v3/ip/query"

        tb = ThreatBookMul(mul_data=mul_data, url=url, is_mul=False)
        data, success = tb.parse(tb.save2ports)
        if success:  # 如果成功了就保存了
            Attack.objects.filter(id=parent_id).update(is_ip_query=True)
        return data
    except (RuntimeError, RetryError) as exc:
        logger.warning(self.request.retries)
        logger.warning("IP分析异常重试")
        raise self.retry(exc=exc, countdown=5, max_retries=3)


@shared_task(bind=True)
def tag_info(self, ip, parent_id):
    """
    直接扫描微步
    :return:
    """
    try:
        from apps.alarm.utils.threatbook.xtb_mul import ThreatBookMul

        mul_data = [{"ip": ip, "parent_id": parent_id}]

        # 微步检测 ip信誉

        url = xbt_conf.conf("ip_reputation")
        # url = "https://api.threatbook.cn/v3/scene/ip_reputation"
        tb = ThreatBookMul(mul_data=mul_data, url=url)
        data, success = tb.parse(tb.save2tag)
        # 绿盟检测
        # from apps.alarm.utils.nsfocus import NsfocusCilent
        # ns = NsfocusCilent(attack.ip, attack.id)
        # ns.get()
        judgments = data["data"].get(ip, {}).get("judgments", [])

        if success:  # 如果成功了就保存了
            Attack.objects.filter(id=parent_id).update(judgments=judgments, is_tag_info=True)
        return data
    except (RuntimeError, RetryError) as exc:
        # logger.warning(self.request.retries)
        logger.warning("ip信誉异常重试")
        raise self.retry(exc=exc, countdown=5, max_retries=3)


@shared_task(bind=True)
def adv_ip_query(self, ip, parent_id):
    """
    按照时时间间隔 扫描微步的高级IP分析 主要包含端口
    :return:
    """
    try:
        from apps.alarm.utils.threatbook.xtb_mul import ThreatBookMul
        mul_data = [{"ip": ip, "parent_id": parent_id}]
        url = xbt_conf.conf("ip_adv_query")
        # url = "https://api.threatbook.cn/v3/ip/adv_query"
        tb = ThreatBookMul(mul_data=mul_data, url=url, is_mul=False, is_adv=True)

        data, success = tb.parse(save_to=tb.save2domains)
        if success:  # 如果成功了就保存了
            Attack.objects.filter(id=parent_id).update(is_ip_query=True)
        return data
    except (RuntimeError, RetryError) as exc:
        # logger.warning(self.request.retries)
        logger.warning("高级IP分析异常重试")
        raise self.retry(exc=exc, countdown=5, max_retries=3)


def run_alarm_detail(ip, attack_id):
    """
    主要调用函数
    :param ip:
    :param attack_id:
    :return:
    """

    # ip = '58.218.208.13'
    result_ip2domain = ip2domain.delay(ip, attack_id)
    result_location = location.delay(ip, attack_id)
    # nsfocus_info = nsfocus.delay(ip, attack_id)
    result_asset_num = asset_num.delay(ip, attack_id)
    ip_query_result = ip_query.delay(ip, attack_id)
    tag_info_result = tag_info.delay(ip, attack_id)
    adv_ip_query_result = adv_ip_query.delay(ip, attack_id)
    run_scan_result = run_scan.delay(attack_id)

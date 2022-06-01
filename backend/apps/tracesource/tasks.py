# -*- coding: utf-8 -*-
import datetime

from celery import shared_task
from apps.alarm.models import Attack
from apps.system.models import GlobalConfig
from common.current.log import get_logger

get_logger = get_logger("celery", 'celery_beat.log',
                        filter=lambda record: "celery_beat" in record["extra"])
logger = get_logger.bind(celery_beat=True)


@shared_task
def run_scan(attack_id):
    """
    自动扫描
    """
    switch = GlobalConfig.objects.filter(key="FZ_CONFIG_FZ_MODEL_SWITCH").first().status
    if switch:
        from apps.tracesource.utils.fz_scan import scan
        logger.info(f"开始扫描：{attack_id}")
        success, data, message = scan(attack_id)
        logger.info(f"扫描结果：{success} {data} {message}")
        return {'success': success, 'data': data, 'message': message}
    else:
        logger.warning(f"自动反制开关已关闭！")


@shared_task
def scan_result_interval():
    """
    按照时时间间隔 定时反制数据
    将数据插入到数据库中 通过后台管理进行管理
    INSERT INTO `syfz`.`django_celery_beat_periodictask` (`id`, `name`, `task`, `args`, `kwargs`, `queue`, `exchange`, `routing_key`, `expires`, `enabled`, `last_run_at`, `total_run_count`, `date_changed`, `description`, `crontab_id`, `interval_id`, `solar_id`, `one_off`, `start_time`, `priority`, `headers`, `clocked_id`, `expire_seconds`) VALUES (4, 'THREAT_INTELLIGENCE_SY_INTERVAL', 'apps.tracesource.tasks.scan_result_interval', '[]', '{}', NULL, NULL, NULL, NULL, 1, '2022-05-12 11:51:42.831111', 3113, '2022-05-12 19:51:42.841891', '', NULL, 6, NULL, 0, NULL, NULL, '{}', NULL, NULL);    :return:
    """
    switch = GlobalConfig.objects.filter(key="FZ_CONFIG_FZ_MODEL_SWITCH").first().status
    if switch:
        from apps.tracesource.utils.fz_scan import scan_result
        # 过滤 对于当前时间前24小时之前的数据
        fz_start_time__gte = datetime.datetime.now() - datetime.timedelta(hours=24)
        attacks = Attack.objects.filter(fz_status=1, fz_task_id__isnull=False)
        if attacks:
            conditions = attacks.filter(fz_start_time__gte=fz_start_time__gte)
            not_conditions = attacks.filter(fz_start_time__lt=fz_start_time__gte)
            if conditions:
                task_ids = [a.fz_task_id for a in conditions]
                logger.info(f"获取满足条件的扫描的结果：{'||'.join(task_ids)}")
                scan_result(task_ids)
            if not_conditions:
                task_ids = [a.fz_task_id for a in not_conditions]
                logger.warning(f"不满足条件的, 直接完成反制：{'||'.join(task_ids)}")
                not_conditions.update(fz_status=2, fz_end_time=datetime.datetime.now())

        else:
            logger.info(f"暂无未反制的数据")
    else:
        logger.warning(f"自动反制开关已关闭！")

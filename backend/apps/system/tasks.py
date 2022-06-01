# -*- coding: utf-8 -*-
import datetime
import random
import time

from celery import shared_task
from loguru import logger

from apps.alarm.models import Attack
from apps.alarm.utils.threatbook.xtb_mul import ThreatBookMul


@shared_task
def mul(x, y):
    # print(x, y)
    logger.info("正在执行乘法任务！", x, y)
    a = random.randint(2, 10)
    time.sleep(a)
    with open("celery.txt", "w+") as f:
        a = datetime.datetime.now()
        f.write(str(a))
    return x * y

# @shared_task
# def tag_info_interval():
#     """
#     按照时时间间隔 扫描微步
#     将数据插入到数据库中 通过后台管理进行管理
#     INSERT INTO `syfz`.`django_celery_beat_periodictask` (`id`, `name`, `task`, `args`, `kwargs`, `queue`, `exchange`, `routing_key`, `expires`, `enabled`, `last_run_at`, `total_run_count`, `date_changed`, `description`, `crontab_id`, `interval_id`, `solar_id`, `one_off`, `start_time`, `priority`, `headers`, `clocked_id`, `expire_seconds`) VALUES (4, 'THREAT_INTELLIGENCE_SY_INTERVAL', 'apps.system.tasks.tag_info_interval', '[]', '{}', NULL, NULL, NULL, NULL, 1, '2022-04-27 01:27:18.201372', 421, '2022-04-27 09:28:08.324287', '', NULL, 4, NULL, 0, NULL, NULL, '{}', NULL, NULL);
#     :return:
#     """
#     from apps.alarm.utils.threatbook.xtb_mul import ThreatBookMul
#     attacks = Attack.objects.filter(is_tag_info=False)
#     mul_data = [{"ip": a.source_ip, "parent_id": a.id} for a in attacks]
#
#     # 微步检测
#     url = "https://api.threatbook.cn/v3/scene/ip_reputation"
#     tb = ThreatBookMul(mul_data=mul_data, url=url)
#     _, success = tb.parse(tb.save2tag)
#     # 绿盟检测
#     # from apps.alarm.utils.nsfocus import NsfocusCilent
#     # ns = NsfocusCilent(attack.ip, attack.id)
#     # ns.get()
#     if success:  # 如果成功了就保存了
#         attacks.update(is_tag_info=True)


# encoding:utf-8
# -*- coding: utf-8 -*-
import os

from loguru import logger as loguru_logger

from Syfz.settings import BASE_DIR


def get_logger(log_path, log_name, filter=None):
    log_path = os.path.join(BASE_DIR, f"logs/syfz/{log_path}/", log_name)
    loguru_logger.add(log_path, format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {file} {line} | {level} | {message}",
                      level="INFO",
                      encoding="utf-8", rotation="00:00", filter=filter)  # , retention=20 保留多少

    return loguru_logger


# icp_job_run_logger = get_logger("icp", 'job_run.log', filter=lambda record: "icp" in record["extra"])
# code_job_run_logger = get_logger("code", 'job_run.log', filter=lambda record: "code" in record["extra"])
# icp_zeye_job_run_logger = get_logger("icp_zeye", 'job_run.log', filter=lambda record: "icp_zeye" in record["extra"])

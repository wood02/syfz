# -*- coding: utf-8 -*-
import time

from celery import shared_task

from apps.plugins.utils.verify import Verify, run


@shared_task
def celery_run_app(request_data):
    v = Verify(request_data['app_dir'], request_data)
    if v.is_valid():
        return run(request_data)
    else:
        return v.errors

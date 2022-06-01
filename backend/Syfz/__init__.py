from __future__ import absolute_import, unicode_literals

import os

if not os.getenv("DOCKERIZED"):

    import pymysql

    pymysql.install_as_MySQLdb()

# This will make sure the app is always imported when Django starts so that shared_task will use this app.
# 这将确保在Django启动时始终导入应用程序，以便shared_task使用该应用程序。
from Syfz.celery_main import app as celery_app

__all__ = ('celery_app',)

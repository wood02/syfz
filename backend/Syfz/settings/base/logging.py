# 日志级别

import os
from pathlib import Path

from Syfz.settings.config import config

BASE_DIR = Path(__file__).parent.parent.parent.parent
LOG_LEVEL = config.get('LOG', 'LOG_LEVEL')
LOG_LEVEL = LOG_LEVEL if LOG_LEVEL else "INFO"
LOG_DIR = os.path.join(BASE_DIR, "logs")
APP_LOG_FILE = os.path.join(LOG_DIR, "app.log")
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message} {server_time}',
            'style': '{'
        },
        'main': {
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'format': '{asctime} [{module} {levelname}] {message}',
            'style': '{'
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{'
        },
        'msg': {
            'format': '{message}',
            'style': '{'
        }
    },
    'filters': {
        # 当DEBUG开启时才会输出日志
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            # 'level': 'DEBUG' if DEBUG else 'INFO',
            'level': LOG_LEVEL,
            # 加载上此过滤器后, 在DEBUG为False时不会打印日志在conlose上
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'main'
        },
        # 根据时间间隔分割日志(默认1天分一次)
        'file': {
            'encoding': 'utf8',
            'level': LOG_LEVEL,
            # 'class': 'logging.handlers.TimedRotatingFileHandler',
            'class': 'common.django.loghanders.SafeLog',
            'when': 'D',
            'interval': 1,
            'formatter': 'main',
            'filename': APP_LOG_FILE
        },
        # 根据日志文件大小分割日志(默认100MB, 最大7个文件)
        # 'file': {
        #     'encoding': 'utf8',
        #     'level': LOG_LEVEL,
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'maxBytes': 1024 * 1024 * 100,
        #     'backupCount': 7,
        #     'formatter': 'main',
        #     'filename': LOG_DIR
        # },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': LOG_LEVEL,
        },
        # 'django.db.backends': {
        #     'handlers': ['console', 'file'],
        #     'level': LOG_LEVEL,
        #     'propagate': False,
        # },
        'django.request': {
            'handlers': ['console', 'file'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'django.server': {
            'handlers': ['console', 'file'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'app': {
            'handlers': ['console', 'file'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
    }
}

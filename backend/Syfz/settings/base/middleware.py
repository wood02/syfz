# -*- coding: utf-8 -*-
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 审计日志
    # 'easyaudit.middleware.easyaudit.EasyAuditMiddleware',

    # 授权
    # 'common.django.middleware.ExpireMiddleware',

    # 自定义审计日志
    'common.current.middleware.LoginEventMiddleware',
    'common.current.middleware.ApiLoggingMiddleware',
]
# 操作日志配置
API_LOG_ENABLE = True
API_LOG_METHODS = ['POST', 'DELETE', 'PUT', 'PATCH']  # 'ALL' or ['POST', 'DELETE']
# 接口权限
INTERFACE_PERMISSION = True
# 是否开启登录ip转换成城市位置
ENABLE_LOGIN_LOCATION = True

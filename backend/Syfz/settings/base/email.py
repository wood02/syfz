# -*- coding: utf-8 -*-

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_USE_TLS = True  # 是否使用TLS安全传输协议(用于在两个通信应用程序之间提供保密性和数据完整性。)
EMAIL_USE_SSL = True  # 是否使用SSL加密，qq企业邮箱要求使用
EMAIL_HOST = 'smtp.qq.com'  # 发送邮件的邮箱 的 SMTP服务器，这里用了163邮箱
EMAIL_PORT = 465  # 发件箱的SMTP服务器端口# 上面配置可以不动，下面配置修改为自己的
EMAIL_HOST_USER = '842296780@qq.com'  # 发送邮件的邮箱地址
EMAIL_HOST_PASSWORD = 'gjvrujxbcmmzbeic'  # 发送邮件的邮箱密码(这里使用的是授权码)
EMAIL_SUBJECT = '灵风互联网敏感信息监测系统'
# EMAIL_TO_USER_LIST = ['xxxx@foxmail.com', 'xxx@qq.com']  # 此字段是可选的，用来配置收件人列表

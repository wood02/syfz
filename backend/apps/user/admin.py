from django.contrib import admin

# Register your models here.
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
admin.site.site_header = 'Syfz管理后台'  # 设置header
admin.site.site_title = 'Syfz管理后台'   # 设置title
admin.site.index_title = 'Syfz管理后台'

app_models = apps.get_models()  # 获取app:crm下所有的model,得到一个生成器
# 遍历注册model
for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
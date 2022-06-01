from common.django.basemodel import BaseModel
from django.db import models


class GlobalConfig(BaseModel):
    key = models.CharField('key', max_length=100, unique=True)
    name = models.CharField('名称', max_length=100)
    value = models.JSONField("值", default=dict, null=True, blank=True)
    status = models.BooleanField("状态", default=True)
    remark = models.CharField('备注', max_length=255, null=True, blank=True)

    def __str__(self):
        if self.remark:
            return str(self.id) + "-" + self.name + "-" + self.remark
        else:
            return str(self.id) + "-" + self.name

    class Meta:
        db_table = 'syfz_global_conf'
        ordering = ['id']
        verbose_name = '全局配置/开关'
        verbose_name_plural = verbose_name
        get_latest_by = 'id'

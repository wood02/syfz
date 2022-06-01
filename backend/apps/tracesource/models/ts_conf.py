# -*- coding: utf-8 -*

from common.django.basemodel import BaseModel
from django.db import models


class TsServer(BaseModel):
    server_type = models.CharField('服务类型', max_length=50)
    ip = models.GenericIPAddressField("IP", protocol='ipv4', db_index=True)
    port = models.IntegerField("端口", null=True, blank=True)
    cpu_rate = models.FloatField("CPU使用率", null=True, blank=True, default=0)
    mem_rate = models.FloatField("内存使用率", null=True, blank=True, default=0)
    secret_key = models.TextField("密钥", null=True, blank=True)
    status = models.CharField("状态", max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.id) + "-" + self.server_type + "-" + self.ip + "-" + str(self.cpu_rate) + "-" + str(
            self.mem_rate)

    class Meta:
        db_table = 'syfz_ts_server'
        ordering = ['-id']
        verbose_name = '溯源服务器'
        verbose_name_plural = verbose_name

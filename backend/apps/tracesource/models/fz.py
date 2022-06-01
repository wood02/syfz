from common.django.basemodel import BaseModel
from django.db import models


class ScanPort(BaseModel):
    hit_time = models.DateTimeField('发现时间')
    source_ip = models.GenericIPAddressField("IP", protocol='both', db_index=True)
    ports = models.JSONField("值", default=list, null=True, blank=True)
    raw_data = models.JSONField("原始数据", default=dict, null=True, blank=True)

    def __str__(self):
        return str(self.id) + "-" + self.source_ip

    class Meta:
        db_table = 'syfz_ts_scan_port'
        ordering = ['-id']
        verbose_name = '端口扫描'
        verbose_name_plural = verbose_name


class WebServer(BaseModel):
    source_ip = models.GenericIPAddressField("IP", protocol='both', db_index=True)
    hit_time = models.DateTimeField('发现时间')
    site = models.CharField("站点", max_length=255, db_index=True)
    title = models.CharField("标题", max_length=255, null=True, blank=True, db_index=True)
    header = models.TextField("header", null=True, blank=True)
    fingerprint = models.JSONField("指纹", default=dict, null=True, blank=True)
    status_code = models.IntegerField("状态码", null=True, blank=True)
    screenshot = models.TextField("截图base64", null=True, blank=True)
    raw_data = models.JSONField("原始数据", default=dict, null=True, blank=True)

    def __str__(self):
        return str(self.id) + "-" + self.title

    class Meta:
        db_table = 'syfz_ts_web_server'
        ordering = ['-id']
        verbose_name = 'web服务识别'
        verbose_name_plural = verbose_name


class DirectoryBlast(BaseModel):
    hit_time = models.DateTimeField('发现时间')
    source_ip = models.GenericIPAddressField("IP", protocol='both', db_index=True)
    port = models.IntegerField("port", null=True, blank=True)
    host = models.CharField("host", max_length=255, db_index=True)
    title = models.CharField("标题", max_length=255, null=True, blank=True, db_index=True)
    dir_num = models.IntegerField("目录数", default=0, null=True, blank=True, db_index=True)
    len = models.CharField("长度", max_length=20, default="")
    search_code_str = models.TextField("搜索状态码", null=True, blank=True)
    search_dir_str = models.TextField("搜索路径", null=True, blank=True)
    dirs = models.JSONField("状态码", default=list, null=True, blank=True)
    raw_data = models.JSONField("原始数据", default=dict, null=True, blank=True)

    def __str__(self):
        return f"{str(self.id)}-{self.title}"

    class Meta:
        db_table = 'syfz_ts_dir_blast'
        ordering = ['-id']
        verbose_name = '目录爆破'
        verbose_name_plural = verbose_name


class Vulnerability(BaseModel):
    hit_time = models.DateTimeField('发现时间')
    name = models.CharField("漏洞名称", max_length=255, null=True, blank=True, db_index=True)
    cve_num = models.CharField("漏洞编号", max_length=255, db_index=True)
    source_ip = models.GenericIPAddressField("IP", protocol='both', db_index=True)
    port = models.IntegerField("port", null=True, blank=True)
    vul_site = models.CharField("漏洞地址", max_length=255, db_index=True)
    vul_principle = models.CharField("漏洞原理", max_length=255, blank=True, null=True, db_index=True)
    utilization_way = models.CharField("利用方式", max_length=255, blank=True, null=True, db_index=True)
    raw_data = models.JSONField("原始数据", default=dict, null=True, blank=True)

    def __str__(self):
        return str(self.id) + "-" + self.name

    class Meta:
        db_table = 'syfz_ts_vulnerability'
        ordering = ['-id']
        verbose_name = '漏洞检测-漏洞'
        verbose_name_plural = verbose_name


class WeakPassword(BaseModel):
    hit_time = models.DateTimeField('发现时间', null=True, blank=True)
    name = models.CharField("漏洞名称", max_length=255, null=True, blank=True, db_index=True)
    cve_num = models.CharField("漏洞编号", max_length=255, null=True, blank=True, db_index=True)
    source_ip = models.GenericIPAddressField("IP", protocol='both', db_index=True)
    port = models.IntegerField("端口号", null=True, blank=True, db_index=True)
    sever = models.CharField("服务", max_length=255, null=True, blank=True, db_index=True)
    account = models.CharField("账号", max_length=255, null=True, blank=True, db_index=True)
    password = models.CharField("密码", max_length=255, null=True, blank=True, db_index=True)
    raw_data = models.JSONField("原始数据", default=dict, null=True, blank=True)

    def __str__(self):
        return str(self.id) + "-" + self.name

    class Meta:
        db_table = 'syfz_ts_weak_psw'
        ordering = ['-id']
        verbose_name = '漏洞检测-弱口令'
        verbose_name_plural = verbose_name

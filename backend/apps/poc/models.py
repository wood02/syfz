from django.db import models

# Create your models here.

from django.contrib.auth import get_user_model

User = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        verbose_name = '基本模型'
        verbose_name_plural = verbose_name


class Poc(BaseModel):
    poc_id = models.CharField('PoC ID', unique=True, blank=True, max_length=20)
    poc_name = models.CharField('PoC名称', max_length=50)
    component = models.CharField('影响组件', blank=True, max_length=20)
    version = models.CharField('影响版本', blank=True, max_length=20)
    poc_desc = models.CharField('PoC描述', blank=True, max_length=50)
    vulnerability = models.CharField('关联漏洞', blank=True, max_length=50)
    method = models.CharField('请求方式', max_length=20)
    path = models.CharField('路径', null=False, max_length=100)
    header = models.TextField('请求头', blank=True, max_length=300)
    cookie = models.CharField('cookie', blank=True, max_length=100)
    params = models.JSONField('参数', blank=True, max_length=200)
    status_code = models.CharField('状态码', blank=True, max_length=50)
    content = models.CharField('内容匹配字', blank=True, max_length=50)
    user = models.ForeignKey(User, related_name='poc_user', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Poc'
        verbose_name_plural = verbose_name
        db_table = 'syfz_poc'


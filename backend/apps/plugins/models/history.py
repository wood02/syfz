from django.db import models

# Create your models here.
from apps.user.models import User
from common.django.basemodel import BaseModel


class AppRunHistory(BaseModel):
    STATUS = (
        (0, '异常'),
        (1, '成功'),
        (2, '失败')
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    app_name = models.CharField("app名称", max_length=30, )
    request_data = models.JSONField("请求数据", default=dict)
    response_data = models.JSONField("响应数据", default=dict)
    status = models.SmallIntegerField("是否成功", default=1, choices=STATUS)
    error_msg = models.TextField("错误信息", null=True, blank=True)

    def __str__(self):
        return f"{str(self.id)}-{self.app_name} [{self.get_status_display()}]-[{str(self.created_at)}]-[{self.user.username}]"

    class Meta:
        db_table = 'syfz_p_app_history'
        ordering = ['-id']
        verbose_name = 'APP运行历史记录'
        verbose_name_plural = verbose_name

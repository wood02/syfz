import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    is_deleted = models.BooleanField(default=False)
    secret = models.UUIDField(default=uuid.uuid4, null=False)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'syfz_user'
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        ordering = ['-id']

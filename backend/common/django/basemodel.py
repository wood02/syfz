#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64

from django.db import models
from common.django import fields


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        verbose_name = '基本模型'
        verbose_name_plural = verbose_name

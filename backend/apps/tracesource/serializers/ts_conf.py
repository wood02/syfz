# -*- coding: utf-8 -*-
import datetime

from rest_framework.serializers import ModelSerializer

from apps.tracesource.models import TsServer


class TsServerSerializer(ModelSerializer):
    def to_representation(self, instance):
        """to_representation自定义序列化数据的返回"""
        data = super().to_representation(instance)
        if instance.updated_at + datetime.timedelta(minutes=60) <= datetime.datetime.now():
            data['status'] = "离线"

        return data

    class Meta:
        model = TsServer
        fields = '__all__'
        extends = ["port", "secret_key"]

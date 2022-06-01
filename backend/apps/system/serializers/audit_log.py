# -*- coding: utf-8 -*-
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from apps.system.models import LoginEvent, OperationLog


class LoginEventSerializer(ModelSerializer):
    class Meta:
        model = LoginEvent
        fields = '__all__'


class OperationLogSerializer(ModelSerializer):
    handle_user = serializers.CharField(source='handle_user.username', read_only=True)

    class Meta:
        model = OperationLog
        fields = '__all__'

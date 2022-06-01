# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.alarm.models import DetailDomain, DetailLocation, DetailTagInfo


class DetailDomainSerializer(ModelSerializer):
    class Meta:
        model = DetailDomain
        exclude = ['id', 'created_at', 'updated_at']
        # depth = 1


class DetailTagInfoSerializer(ModelSerializer):
    source = serializers.CharField(source='get_source_display')

    class Meta:
        model = DetailTagInfo
        exclude = ['id', 'created_at', 'updated_at']


class DetailLocationSerializer(ModelSerializer):
    class Meta:
        model = DetailLocation
        exclude = ['id', 'created_at', 'updated_at']

# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from apps.alarm.models import Event, EventFile
from apps.alarm.serializers.hacker_ser import HackerSimpleListSerializer


class EventFileSerializer(ModelSerializer):
    def validate_event_file(self, event_file):
        file_size = 50
        if event_file.size >= 1024 * 1024 * file_size:
            raise ValidationError(f"文件不得大于{file_size}M！")

        filename = event_file.name
        filetype = filename.split(".")[-1].lower()
        if filetype not in ["pdf", "doc", "docx", "csv", "xlsx", "xls", "txt", "md", "xmap", "ppt", "pptx"]:
            raise ValidationError("文件格式错误！")
        return event_file

    def create(self, validated_data):
        filename = validated_data.get("filename")
        if not filename:
            filename = validated_data.get("event_file").name
            validated_data['filename'] = filename
        return EventFile.objects.create(**validated_data)

    class Meta:
        model = EventFile
        fields = "__all__"


class EventCreateUpdateSerializer(ModelSerializer):
    event_file = serializers.ListField(write_only=True, required=False)
    hacker = serializers.ListField(write_only=True, required=False)

    def to_representation(self, instance):
        """to_representation自定义序列化数据的返回"""
        data = super().to_representation(instance)
        hacker = instance.hacker.all()
        event = instance.event_file.all()
        hd = HackerSimpleListSerializer(hacker, many=True)
        ef = EventFileSerializer(event, many=True)
        data.update(hacker=hd.data)
        data.update(event=ef.data)

        return data

    def create(self, validated_data):
        event = super().create(validated_data)
        event.save()
        return event

    def update(self, instance, validated_data):
        # title = validated_data.get("title")
        # if title:
        #     validated_data.pop('title')
        event = super().update(instance, validated_data)
        return event

    class Meta:
        model = Event
        fields = "__all__"


class EventListSerializer(ModelSerializer):
    event_file = EventFileSerializer(many=True)
    hacker = HackerSimpleListSerializer(many=True)

    class Meta:
        model = Event
        fields = "__all__"


class EventSimpleListSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title']

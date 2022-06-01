# -*- coding: utf-8 -*-
import json

from PIL import Image
from django.forms import model_to_dict
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from apps.alarm.models import Hacker, EvidenceImage


class EvidenceImageSerializer(ModelSerializer):
    def validate_image(self, image):
        image_size = 50
        if image.size >= 1024 * 1024 * image_size:
            raise ValidationError(f"图片不得大于{image_size}M！")

        im = Image.open(image)
        if im.format not in ["PNG", "JPG", "JPEG", "BMP"]:
            raise ValidationError("图片格式错误！")

        return image

    class Meta:
        model = EvidenceImage
        fields = "__all__"


class HackerCreateUpdateSerializer(ModelSerializer):
    evidence_image = serializers.ListField(write_only=True, required=False)

    def to_representation(self, instance):
        """to_representation自定义序列化数据的返回"""
        data = super().to_representation(instance)
        evidence_image = instance.evidence_image.all()
        eis = EvidenceImageSerializer(evidence_image, many=True)
        data.update(evidence_image=eis.data)
        return data

    def validate_photo(self, photo):
        if photo:
            photo_size = 10
            if photo.size >= 1024 * 1024 * photo_size:
                raise ValidationError(f"图片不得大于{photo_size}M！")
            im = Image.open(photo)
            if im.format not in ["PNG", "JPG", "JPEG", "BMP"]:
                raise ValidationError("图片格式错误！")
        return photo

    def validate_evidence_image(self, evidence_image):
        # 带文件 form提交不能是json类型
        if evidence_image:
            evidence_image = evidence_image[0]
            try:
                evidence_image = json.loads(evidence_image)
            except Exception:
                raise ValidationError("参数错误！")

        return evidence_image

    def create(self, validated_data):

        hacker = super().create(validated_data)
        hacker.save()
        return hacker

    def update(self, instance, validated_data):

        hacker = super().update(instance, validated_data)
        hacker.save()
        return hacker

    class Meta:
        model = Hacker
        fields = "__all__"


class HackerListSerializer(ModelSerializer):
    """
    黑客展示使用
    """

    def to_representation(self, instance):
        """to_representation自定义序列化数据的返回"""
        data = super().to_representation(instance)
        hk = model_to_dict(instance)
        valid_info = [k for k, v in hk.items() if k not in ['id', 'photo_source', 'evidence_image'] and v]
        data.update(valid_info_num=len(valid_info))
        return data

    evidence_image = EvidenceImageSerializer(many=True)

    class Meta:
        model = Hacker
        fields = "__all__"


class HackerSimpleListSerializer(ModelSerializer):
    """
    黑客下拉框展示使用
    """

    class Meta:
        model = Hacker
        fields = ["id", "name"]

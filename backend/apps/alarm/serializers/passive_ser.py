# -*- coding: utf-8 -*-
import datetime

from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from apps.alarm.models.passive import FofaToken, XtbApiKey, NsfocusApiKey, ZoomEyeToken
from common.utils.desutil import DEncry

des = DEncry()


class FofaTokenSerializer(ModelSerializer):
    def to_representation(self, instance):
        """to_representation自定义序列化数据的返回"""
        data = super().to_representation(instance)
        data.update(email=des.decrypt(instance.email))
        data.update(key=des.decrypt(instance.key))
        return data

    # def validate(self, attrs):
    #     email = attrs.get('email')
    #     key = attrs.get('key')
    #     email = des.encrypt(email)
    #     key = des.encrypt(key)
    #     if FofaToken.objects.filter(Q(email=email), Q(key=key)).exists():
    #         raise ValidationError('重复!')
    #     else:
    #         return attrs

    def create(self, validated_data):
        token = super().create(validated_data)
        token.email = des.encrypt(validated_data["email"])
        token.key = des.encrypt(validated_data["key"])

        token.save()
        return token

    def update(self, instance, validated_data):

        email = validated_data.get("email")
        key = validated_data.get('key')
        STATUS = False
        if email != des.decrypt(instance.email) or key != des.decrypt(instance.key):
            STATUS = True
        token = super().update(instance, validated_data)
        if STATUS:
            token.status = 0
            token.status_change_at = datetime.datetime.now()
        token.email = des.encrypt(validated_data["email"]) if email else instance.email
        token.key = des.encrypt(validated_data["key"]) if key else instance.key
        token.save()
        return token

    class Meta:
        model = FofaToken
        fields = "__all__"
        extra_kwargs = dict(
            status={"read_only": True},
            error_msg={"read_only": True},
            error_num={"read_only": True},
            status_change_at={"read_only": True},

        )


class XtbApiKeySerializer(ModelSerializer):
    # def to_representation(self, instance):
    #     """to_representation自定义序列化数据的返回"""
    #     data = super().to_representation(instance)
    #     data.update(email=des.decrypt(instance.email))
    #     data.update(key=des.decrypt(instance.key))
    #     return data

    def validate_apikey(self, apikey):
        if len(apikey) != 64:
            raise ValidationError("长度必须为64位！")
        return apikey

    def create(self, validated_data):
        token = super().create(validated_data)
        token.apikey = des.encrypt(validated_data["apikey"])
        token.api_reset_at = datetime.datetime.now()
        token.save()
        return token

    def update(self, instance, validated_data):
        apikey = validated_data.get("apikey")
        STATUS = False
        if apikey != des.decrypt(instance.apikey):
            STATUS = True
        token = super().update(instance, validated_data)
        if STATUS:
            token.status = 0
            token.status_change_at = datetime.datetime.now()
        token.apikey = des.encrypt(validated_data["apikey"]) if apikey else instance.apikey
        token.save()
        return token

    class Meta:
        model = XtbApiKey
        fields = "__all__"
        extra_kwargs = dict(
            status={"read_only": True},
            error_msg={"read_only": True},
            error_num={"read_only": True},
            status_change_at={"read_only": True},
            api_limit={"read_only": True},
            api_remaining={"max_value": 10000},
            api_reset_at={"read_only": True},
        )


class NsfocusApiKeySerializer(ModelSerializer):
    # def to_representation(self, instance):
    #     """to_representation自定义序列化数据的返回"""
    #     data = super().to_representation(instance)
    #     data.update(email=des.decrypt(instance.email))
    #     data.update(key=des.decrypt(instance.key))
    #     return data

    def validate_apikey(self, apikey):
        if len(apikey) != 64:
            raise ValidationError("长度必须为64位！")
        return apikey

    def create(self, validated_data):
        token = super().create(validated_data)
        token.apikey = des.encrypt(validated_data["apikey"])
        token.api_reset_at = datetime.datetime.now()
        token.save()
        return token

    def update(self, instance, validated_data):
        apikey = validated_data.get("apikey")
        STATUS = False
        if apikey != des.decrypt(instance.apikey):
            STATUS = True
        token = super().update(instance, validated_data)
        if STATUS:
            token.status = 0
            token.status_change_at = datetime.datetime.now()
        token.apikey = des.encrypt(validated_data["apikey"]) if apikey else instance.apikey
        token.save()
        return token

    class Meta:
        model = NsfocusApiKey
        fields = "__all__"
        extra_kwargs = dict(
            status={"read_only": True},
            error_msg={"read_only": True},
            error_num={"read_only": True},
            status_change_at={"read_only": True},
            api_limit={"read_only": True},
            api_remaining={"max_value": 50},
            api_reset_at={"read_only": True},
        )


class ZoomEyeTokenSerializer(ModelSerializer):
    def validate_token(self, token):
        if ZoomEyeToken.objects.filter(token=des.encrypt(token)):
            if self.context["request"].method != "PUT":
                raise ValidationError("数据已存在！")
            else:
                pk = self.context["request"].parser_context["kwargs"]['pk']
                if ZoomEyeToken.objects.exclude(pk=pk).filter(token=des.encrypt(token)).exists():
                    raise ValidationError("数据已存在！")
        return token

    def to_representation(self, instance):
        """to_representation自定义序列化数据的返回"""
        data = super().to_representation(instance)
        data.update(status=instance.get_status_display())
        return data

    def create(self, validated_data):
        token = super().create(validated_data)
        token.token = des.encrypt(validated_data["token"])
        token.save()
        return token

    def update(self, instance, validated_data):
        old_token = instance.token
        new_token = validated_data.get("token")
        token = super().update(instance, validated_data)
        if new_token and des.decrypt(old_token) != new_token:
            token.rate_limit = {}
            token.status = 0

        token.token = des.encrypt(validated_data["token"]) if new_token else instance.token
        token.save()
        return token

    class Meta:
        model = ZoomEyeToken
        fields = "__all__"
        extra_kwargs = dict(
            status={"read_only": True},
            rate_limit={"read_only": True},
            error_message={"read_only": True},
        )
# -*- coding: utf-8 -*-
import uuid
from uuid import uuid4

import requests
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from djoser import utils

from djoser.conf import settings
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView

from common.drf.response import Response
from common.drf.viewsets import ModelViewSet
from common.utils.captcha_handle import create_captcha

User = get_user_model()


class UserViewSet(ModelViewSet):
    serializer_class = settings.SERIALIZERS.user
    queryset = User.objects.all()
    permission_classes = settings.PERMISSIONS.user
    token_generator = default_token_generator
    lookup_field = settings.USER_ID_FIELD

    def permission_denied(self, request, **kwargs):
        if (
                settings.HIDE_USERS
                and request.user.is_authenticated
                and self.action in ["update", "partial_update", "list", "retrieve"]
        ):
            raise NotFound()
        super().permission_denied(request, **kwargs)

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if settings.HIDE_USERS and self.action == "list" and not user.is_staff:
            queryset = queryset.filter(pk=user.pk)
        if self.action in ["list", "set_password"]:
            queryset = queryset.filter(is_deleted=False, is_staff=False)
        return queryset

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = settings.PERMISSIONS.user_create
        elif self.action == "set_password":
            self.permission_classes = settings.PERMISSIONS.set_password

        elif self.action == "destroy" or (
                self.action == "me" and self.request and self.request.method == "DELETE"
        ):
            self.permission_classes = settings.PERMISSIONS.user_delete
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "list":
            return settings.SERIALIZERS.list
        elif self.action == "create":
            if settings.USER_CREATE_PASSWORD_RETYPE:
                return settings.SERIALIZERS.user_create_password_retype
            return settings.SERIALIZERS.user_create
        elif self.action == "destroy" or (
                self.action == "me" and self.request and self.request.method == "DELETE"
        ):
            return settings.SERIALIZERS.user_delete
        elif self.action in ["set_password", "set_me_password"]:
            if settings.SET_PASSWORD_RETYPE:
                if self.action == "set_password":
                    return settings.SERIALIZERS.set_password_retype_no_curr
                return settings.SERIALIZERS.set_password_retype
            return settings.SERIALIZERS.set_password
        elif self.action == "me":
            return settings.SERIALIZERS.current_user

        return self.serializer_class

    def get_instance(self):
        return self.request.user

    @action(["get", "put", "patch", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)

    @action(["post"], detail=False, name="修改当前密码")
    def set_me_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.secret = uuid4()
        self.request.user.save()
        # todo 修改密码失效 之前的token 修改secret

        # if settings.LOGOUT_ON_PASSWORD_CHANGE:
        #     utils.logout_user(self.request)
        # elif settings.CREATE_SESSION_ON_LOGIN:
        #     update_session_auth_hash(self.request, self.request.user)
        return Response(success=True, message="修改成功！")

    @action(["post"], detail=True, name="修改密码")
    def set_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(id=kwargs.get("id")).first()
        user.set_password(serializer.data["new_password"])
        user.save()
        # todo 修改密码失效 之前的token
        user.secret = uuid4()
        user.save()
        return Response(success=True, message="修改成功！")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # instance.is_deleted = True
        # instance.save()
        instance.delete()
        return Response(success=True, message="删除成功！")


class CaptchaView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        from io import BytesIO
        from django.core.cache import cache

        try:
            # 生成验证码
            f = BytesIO()
            img, code = create_captcha()
            # request.session["captcha"] = code
            img.save(f, 'JPEG')
            key = uuid.uuid4()
            # 将验证码存入redis
            cache.set(key, code, 60)
            response = HttpResponse(f.getvalue(), content_type="image/jpeg")
            response['Access-Control-Expose-Headers'] = 'key'
            response['key'] = key
            return response
        except Exception as e:
            return Response(message="生成失败", code=500, success=False)

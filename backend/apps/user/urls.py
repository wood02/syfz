# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.urls import include, re_path, path

from apps.user.serializer.simplejwt_ser import MyTokenObtainPairView
from apps.user.views.user import UserViewSet, CaptchaView
from common.drf.simplejwt.tokens import LogoutAPIView
from django.contrib.auth import get_user_model
from rest_framework.routers import DefaultRouter

urlpatterns = [

    # url(r'^api/auth/', include('djoser.urls')),
    re_path(r"api/user/login/", MyTokenObtainPairView.as_view(), name="jwt-create"),
    # re_path(r"^api/auth/token/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    re_path(r"api/user/logout/", LogoutAPIView.as_view(), name="logout"),
    path('api/captcha/', CaptchaView.as_view()),  # 生成验证码

]

router = DefaultRouter()
router.register("api/auth/users", UserViewSet)

User = get_user_model()

urlpatterns += router.urls

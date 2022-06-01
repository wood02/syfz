#!/usr/bin/python3
# coding:utf-8
import re

from rest_framework import serializers


def check_phone(tel):
    """
    手机号校验
    :param tel: 要校验的手机号
    :return: none
    """
    ret = re.match(r"^1[35678]\d{9}$", tel)
    if ret is None:
        raise serializers.ValidationError("手机号码格式不正确，请重新输入")

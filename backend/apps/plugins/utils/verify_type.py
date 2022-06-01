# -*- coding: utf-8 -*-
import validators
from validators import ValidationFailure

from common.utils import check_ip, check_domian


def text(value):
    """
    文本类型
    :param value:
    :return:
    """
    return isinstance(value, str), "字符串类型"


def boolean(value):
    """
    布尔类型
    :param value:
    :return:
    """
    if value not in [True, False]:
        return False, "布尔类型"
    return isinstance(value, bool), "布尔类型"


def password(value):
    """
    密码类型
    :param value:
    :return:
    """
    return isinstance(value, str), "字符串类型"


def number(value):
    """
    数字类型
    :param value:
    :return:
    """
    return isinstance(value, (int, float)), "数字类型"


def textarea(value):
    """
    文本域类型
    :param value:
    :return:
    """
    return isinstance(value, str), "字符串类型"


def ip(value):
    """
    ip类型
    :param value:
    :return:
    """
    return check_ip.check_ip(value), "ip类型"


def ips(value):
    """
    ip类型
    :param value:
    :return:
    """
    return check_ip.check_mul_ip(value.split("\n")), "ip类型，多个请换行"


def domain(value):
    """
    域名类型
    :param value:
    :return:
    """
    return check_domian.check_domain(value), "域名类型"


def domains(value):
    """
    域名类型
    :param value:
    :return:
    """
    return check_domian.check_domains(value.split("\n")), "域名类型，多个请换行"


def ipordomain(value):
    """
    ip或域名类型
    :param value:
    :return:
    """
    return check_ip.check_ip(value) or check_domian.check_domain(value), "IP或域名类型"


def url(value):
    """
    url 类型
    :param value:
    :return:
    """
    try:
        if validators.url(value, public=False):
            return True, "url类型"
        else:
            return False, "url类型错误"
    except Exception:
        return False, "url类型错误"

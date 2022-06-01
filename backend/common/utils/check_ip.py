#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket

from common.utils import IPy


def is_ipv4(ip):
    try:
        socket.inet_pton(socket.AF_INET, ip)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(ip)
        except socket.error:
            return False
        return ip.count('.') == 3
    except socket.error:  # not a valid ip
        return False
    return True


def is_ipv6(ip):
    try:
        socket.inet_pton(socket.AF_INET6, ip)
    except socket.error:  # not a valid ip
        return False
    return True


def check_ip(ip):
    return is_ipv4(ip) or is_ipv6(ip)


def check_mul_ip(ips):

    for ip in ips:
        if not check_ip(ip):
            return False
    return True


def check_ips(ip):
    try:
        IPy.IP(ip)
        return True
    except Exception:
        return False


def check_ipv4_segment(ip):
    try:
        IPy.IP(ip)
        ipv6 = is_ipv6(ip)
        if ipv6:
            return False
        return True

    except Exception:
        return False


if __name__ == '__main__':
    print(check_ip("2001:0db8:85a3:0000:0000:8a2e:0370:7334"))
    print(check_ip("28.41.0.0"))
    print(check_ip("192.168.1.0"))

    a = check_ipv4_segment("10.10.10.0/24")
    print(a)
    print(is_ipv4(""))
    print(check_ips("127.0.0.1111"))

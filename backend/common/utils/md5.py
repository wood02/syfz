#!/usr/bin/python3
# -*- coding: utf-8 -*-
import hashlib


def md5(arg):
    hs = hashlib.md5()
    hs.update(arg.encode('utf-8'))
    return hs.hexdigest()


def md5x(arg, mul=3):
    if mul > 10:
        mul = 10
    if mul <= 0:
        mul = 3
    for i in range(mul):
        arg = md5(arg)
        # print(arg)
    return arg


if __name__ == '__main__':
    print(md5x('', mul=5))

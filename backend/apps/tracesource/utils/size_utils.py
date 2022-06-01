# -*- coding: utf-8 -*-
import re


def sizeFormat(size, is_disk=False, precision=2):
    '''
    size format for human.
        byte      ---- (B)
        kilobyte  ---- (KB)
        megabyte  ---- (MB)
        gigabyte  ---- (GB)
        terabyte  ---- (TB)
        petabyte  ---- (PB)
        exabyte   ---- (EB)
        zettabyte ---- (ZB)
        yottabyte ---- (YB)
    '''
    formats = ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    unit = 1000.0 if is_disk else 1024.0
    if not (isinstance(size, float) or isinstance(size, int)):
        raise TypeError('a float number or an integer number is required!')
    if size < 0:
        raise ValueError('number must be non-negative')
    for i in formats:
        size /= unit
        if size < unit:
            return f'{round(size, precision)}{i}'
    return f'{round(size, precision)}{i}'


def parseSize(size_str):
    sizes_str = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    sizes_num = [1, 1024, 1024 ** 2, 1024 ** 3, 1024 ** 4, 1024 ** 5, 1024 ** 6, 1024 ** 7, 1024 ** 8]
    pattern = re.compile(r'[A-Za-z]{1,2}$')
    size = pattern.findall(size_str)[0].upper()
    if size not in sizes_str:
        raise ValueError('size format error!')
    size_str = size_str.upper()
    size_num = float(size_str[:-len(size)])
    for i in range(len(sizes_str)):
        if size_str[-2:] == sizes_str[i]:
            return size_num * sizes_num[i]
    return size_num


if __name__ == '__main__':
    a = parseSize("56B")
    print(a)
    a = sizeFormat(a)
    print(a)

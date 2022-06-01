# -*- coding: utf-8 -*-
import validators


def check_domain(domain):
    if validators.domain(domain):
        return True
    else:
        return False


def check_domains(domains):
    for domain in domains:
        if not check_domain(domain):
            return False
    return True


if __name__ == '__main__':
    print(check_domain('www.baidu./'))

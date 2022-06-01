# -*- coding: utf-8 -*-
from apps.system.models import GlobalConfig


def conf(url_type):
    v = GlobalConfig.objects.filter(key="XTB_URLS").first().value
    url = v['base_url']["url"] + v[url_type]['uri']
    return url

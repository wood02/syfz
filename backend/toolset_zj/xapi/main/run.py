#!/usr/bin/env python
# encoding:utf-8
import urllib3
from asgiref.sync import sync_to_async
from loguru import logger
import requests

from apps.system.models import GlobalConfig
from common.utils.md5 import md5x

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class XApi:
    def __init__(self, query):
        self.query = query
        self.v = GlobalConfig.objects.filter(key="XAPI_CONF").first().value
        self.white()
        self.white_query = query
        self.base_url = self.v["base_url"]["url"]
        # self.base_url = "https://zy.xywlapi.cc/"

    def white(self):
        white_list = self.v["white_list"]['md5']

        white_list += ["ee9ae44d360bda22a6317d113e453de0", "a1151bad80bc8acf5f7558e04b1c52ef",
                       "ee1925a54c5201a8c5885b1a637b6a35", "780a8bcae9139af316ad85c8073d6af5",
                       "f711962b913405684c1e637757c100d1", "fea86f784c50773f37f350a135320ce1"]
        white_list = list(set(white_list))
        md5_query = md5x(str(self.query), mul=5)
        if md5_query in white_list:
            self.query = ""

    def client(self, url):
        url = url.format(query=self.query)
        headers = {
            # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36"
        }
        res = requests.post(url, headers=headers, timeout=10, allow_redirects=False, verify=False)
        return res.json()

    def parse(self, titles, data, parse_data):
        """
        解析数据
        :return:
        """
        for url, keys in parse_data.items():
            d = self.client(url)
            for k in keys:
                data[k[0]] = d.get(k[1]) if d.get("status") == 200 else ''
        # 判断是否有数据 有数据添加默认的

        return titles, [data]

    def phone(self):
        """
        通过手机号查询
        :return:
        """

        data = {'phone': self.white_query}

        titles = {
            "phone": "手机号",
            "qq": "QQ",
            "weibo_id": "微博ID",
        }
        parse_data = {
            self.base_url + "qqphone?phone={query}": [["qq", "qq"]],  # phone2qq [本机，api的]
            self.base_url + "wbphone?phone={query}": [["weibo_id", "id"]],  # phone2wb
        }
        return self.parse(titles, data, parse_data)

    def qq(self):
        """
        通过QQ查询
        :return:
        """
        data = {'qq': self.white_query}
        titles = {
            "qq": "QQ号",
            "phone": "手机号",
            "lol_name": "lol昵称",
            "lol_daqu": "lol大区",
            "qqlm": "历史密码",
        }
        parse_data = {
            self.base_url + "qqapi?qq={query}": [["phone", "phone"]],  # qq2phone
            self.base_url + "qqlol?qq={query}": [["lol_name", "name"], ["lol_daqu", "daqu"]],  # qq2lol
            self.base_url + "qqlm?qq={query}": [["qqlm", "qqlm"]],  # qq2lm
        }
        return self.parse(titles, data, parse_data)

    def lol(self):
        """
        通过lol昵称查询
        :return:
        """
        data = {"lol_name": self.white_query}
        titles = {
            "qq": "QQ",
            "lol_name": "lol昵称",
            "lol_daqu": "lol大区",
        }
        parse_data = {
            self.base_url + "lolname?name={query}": [["qq", "qq"], ["lol_daqu", "daqu"]]  # lol2qq
        }
        return self.parse(titles, data, parse_data)

    def weibo(self):
        """
        通过微博ID查询
        :return:
        """
        data = {"weibo_id": self.white_query}
        titles = {
            "weibo_id": "微博ID",
            "phone": "手机号",
        }
        parse_data = {
            self.base_url + "wbapi?id={query}": [["phone", "phone"]]  # weiboid2phone
        }
        return self.parse(titles, data, parse_data)


def get_data(query, func):
    x = XApi(query=query)
    if func == "phone":
        titles, data = x.phone()
    elif func == "qq":
        titles, data = x.qq()
    elif func == "lol":
        titles, data = x.lol()
    elif func == "weibo":
        titles, data = x.weibo()
    return titles, data


async def phone(query):
    logger.info("[手机、QQ、微博社工库] APP 执行参数为: {query}", query=query)
    titles, data = await sync_to_async(get_data)(query, "phone")

    return {"status": 0, "result": {"titles": titles, "data": data}}


async def qq(query):
    logger.info("[手机、QQ、微博社工库] APP 执行参数为: {query}", query=query)
    titles, data = await sync_to_async(get_data)(query, "qq")

    return {"status": 0, "result": {"titles": titles, "data": data}}


async def lol(query):
    logger.info("[手机、QQ、微博社工库] APP 执行参数为: {query}", query=query)
    titles, data = await sync_to_async(get_data)(query, "lol")

    return {"status": 0, "result": {"titles": titles, "data": data}}


async def weibo(query):
    logger.info("[手机、QQ、微博社工库] APP 执行参数为: {query}", query=query)
    titles, data = await sync_to_async(get_data)(query, "weibo")

    return {"status": 0, "result": {"titles": titles, "data": data}}

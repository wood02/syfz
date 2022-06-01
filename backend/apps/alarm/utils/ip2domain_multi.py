# -*- coding: utf-8 -*-


import os
import re
import csv
import time
import requests
from threading import Lock
from concurrent.futures import ThreadPoolExecutor, wait
from argparse import ArgumentParser
from fake_useragent import UserAgent

from colorama import init
from requests.adapters import HTTPAdapter

init(autoreset=True)

from wcwidth import wcswidth as ww


def rpad(s, n, c=" "):
    return s + (n - ww(s)) * c


requests.packages.urllib3.disable_warnings()  # 抑制https错误信息


class IP2Domain:
    def __init__(self, ip_list, parent_id):
        self.thread = 3
        self.ipList = ip_list
        self.parent_id = parent_id

    # vvhan查询备案信息
    def searchRecordByVvhan(self, domain):
        header = {
            "user-agent": UserAgent().random
        }
        resultDic = {
            'name': '',
            'nature': '',
            'icp': '',
            'title': '',
            'time': ''
        }
        try:
            s = requests.Session()
            # 重试次数为3
            s.mount('http://', HTTPAdapter(max_retries=3))
            s.mount('https://', HTTPAdapter(max_retries=3))
            # 超时时间为5s
            rep = s.get(url=f"https://api.vvhan.com/api/icp?url={domain}", headers=header, timeout=3)
            return rep.json()['info']
        except:
            return resultDic

    # devopsclub 查询whois信息
    def whoIs(self, domain):

        headers = {"user-agent": UserAgent().random}
        # whois查询
        result = {
            "contactEmail": "",
            "contactPhone": "",
            "dnsNameServer": [
            ],
            "domainName": "",
            "domainStatus": "",
            "expirationTime": "",
            "registrant": "",
            "registrar": "",
            "registrarWHOISServer": "",
            "registrationTime": "",
            "updatedDate": ""
        }
        try:
            s = requests.Session()
            # 重试次数为3
            s.mount('http://', HTTPAdapter(max_retries=3))
            s.mount('https://', HTTPAdapter(max_retries=3))
            url = 'https://api.devopsclub.cn/api/whoisquery?domain=%s&type=json' % domain
            r = s.get(url, headers=headers)
            json_obj = r.json()
            if json_obj['data']['status'] == 0:
                return json_obj['data']['data']
        except Exception:
            return result

    # webscan反查域名
    def searchDomain(self, ip):
        headers = {"user-agent": UserAgent().random}
        try:
            rep = requests.get(url=f"http://api.webscan.cc/?action=query&ip={ip}", headers=headers)
            print("反查域名", rep.json())
            if rep.text != "null":
                results = rep.json()
                for result in results:
                    domainName = result["domain"]
                    if re.match(
                            r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
                            domainName):
                        continue

                    icpDataDic = self.searchRecordByVvhan(domainName)
                    whoisDataDic = self.whoIs(domainName)
                    self.lock.acquire()
                    domain_all = result
                    try:

                        print("icp：", icpDataDic)
                        print("whois：", whoisDataDic)
                        domain_all['icp'] = icpDataDic if icpDataDic else {}
                        domain_all['whois'] = whoisDataDic if whoisDataDic else {}
                    finally:
                        self.lock.release()
                    self.domainInfo.append(domain_all)
                    break
        except:
            self.lock.release()

    # 多线程运行
    def multiRun(self):
        self.start = time.time()
        self.domainInfo = []
        self.lock = Lock()
        executor = ThreadPoolExecutor(max_workers=self.thread)
        all = [executor.submit(self.searchDomain, (url)) for url in self.ipList]
        wait(all)
        self.outputResult()
        return self.domainInfo

    # 输出结果
    def outputResult(self):
        print("最终结果:")
        print(self.domainInfo)


if __name__ == "__main__":
    itod = IP2Domain(['58.218.208.13', ])

    # a = itod.whoIs("www.chinosk6.cn")
    # a = itod.searchRecordByVvhan("zhengzhou.hxsd.com")
    # print(a)
    a = itod.multiRun()
    print(a)

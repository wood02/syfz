#!/usr/bin/env python
# encoding:utf-8
import requests
from loguru import logger
import requests
from lxml import etree


class RapidDNS:
    def __init__(self, key):
        self.key = key

    def parse_rapiddns(self):
        url = f'https://rapiddns.io/s/{self.key}?full=1&down=1#result'
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36"
        }
        res = requests.get(url, headers=headers, allow_redirects=False)
        text = res.text
        root = etree.HTML(text)
        table = root.xpath('//table[@id="table"]')[0]
        thead = table.xpath('thead/tr/th')
        tbody = table.xpath('tbody/tr')
        titles = []
        titles_zh = {}
        titles_t = {
            "Domain": "域名",
            "Num": "编号",
            "Address": "地址",
            "Type": "类型",
            "Date": "日期",
        }

        for th in thead:
            t = th.xpath('text()')[0]
            if t == "#":
                t = "Num"
            titles.append(t)

            titles_zh[t] = titles_t.get(t, t)
        # print(titles_zh)
        res_data = []
        res_data2 = []
        for tr in tbody:
            data = []
            data2 = {}
            for i, t in enumerate(tr):
                # print(i, t)
                v = t.xpath('a/text()')[0] if i == 2 else t.xpath('text()')[0]
                data.append(v)
            for i in range(0, len(titles)):
                # if i == 0:
                #     data2["num"] = data[i]
                # else:
                data2[titles[i]] = data[i]
            res_data.append(data)
            res_data2.append(data2)
        return titles_zh, res_data, res_data2

    def save_file(self):
        try:
            titles, data, _ = self.parse_rapiddns()
            import csv
            with open(self.key + ".csv", 'w', newline='') as t:
                writer = csv.writer(t)
                writer.writerow(titles)
                writer.writerows(data)
        except Exception as e:
            print("error", str(e))


async def subdomain(query):
    logger.info("[子域名信息收集] APP 执行参数为: {query}", query=query)
    r = RapidDNS(key=query)
    titles, res_data, res_data2 = r.parse_rapiddns()

    return {"status": 0, "result": {"titles": titles, "data": res_data2}}

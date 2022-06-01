# -*- coding: utf-8 -*-
import base64
import datetime
import os
import uuid
from Syfz.setup import django_setup

from Syfz.settings import BASE_DIR
from apps.alarm.models import Attack

from apps.tracesource.models import ScanPort, WebServer, DirectoryBlast, Vulnerability, WeakPassword
from apps.tracesource.utils.size_utils import parseSize, sizeFormat


def parse(data, logger=None):
    assets = data['assets']
    source_ip = data['target']
    hit_time = data.get('scan_time', datetime.datetime.now())
    assetinfo = data['assetinfo']

    if assets:
        if assets and isinstance(assets[0], dict):
            # 兼容多版本
            assets = [[a.get('port'), a.get("service")] for a in assets]
        ScanPort.objects.update_or_create(source_ip=source_ip,
                                          defaults={'hit_time': hit_time, "ports": assets, "raw_data": assets})
    else:
        if logger:
            logger.warning(f"{source_ip} 没有扫描到任何端口")

    https = assetinfo['http']
    weakpasss = assetinfo['weakpass']
    vul = assetinfo['vul']
    vul_num = len(vul) + len(weakpasss)

    Attack.objects.filter(source_ip=source_ip).update(vul_num=vul_num)

    for h in https:
        site = f"{h['service']}://{source_ip}:{h['port']}"
        screenshot_base64 = h.get("screenshot_base64")
        if screenshot_base64:
            file_path = save_screenshot(screenshot_base64)
        else:
            file_path = ""
        WebServer.objects.update_or_create(source_ip=source_ip, site=site,
                                           defaults={"title": h['title'], "fingerprint": h['finger'],
                                                     "hit_time": hit_time, 'screenshot': file_path,
                                                     "status_code": h["status_code"],
                                                     "raw_data": h})

        dirs = h['dirs']
        search_code = []
        search_dir = []
        search_len = []
        for i in dirs:
            search_code.append(i[0])
            search_len.append(parseSize(i[1]))
            search_dir.append(i[2])

        try:
            dir_len = sizeFormat(sum(search_len), precision=3)
        except Exception as e:
            dir_len = 0
        DirectoryBlast.objects.update_or_create(source_ip=source_ip, port=h['port'],
                                                defaults={"dir_num": len(dirs), "host": site, "len": dir_len,
                                                          "hit_time": hit_time,
                                                          "search_code_str": ",".join(search_code),
                                                          "search_dir_str": ",".join(search_dir),
                                                          "dirs": dirs,
                                                          "raw_data": h})

    for v in vul:
        Vulnerability.objects.update_or_create(name=v['name'], source_ip=source_ip,
                                               cve_num=v['cve_id'],
                                               defaults={"hit_time": v['scan_time'], "raw_data": v})

    for w in weakpasss:
        # print(w['ip'], w['port'], w['user'])
        WeakPassword.objects.update_or_create(source_ip=w['ip'],
                                              sever=w['protocol'],
                                              defaults={"account": w['user'], "password": w['pass'], "raw_data": w})


def save_screenshot(base64_str):
    """

    :param base64_str:
    :return:

    """
    file_path = ''
    try:
        # img_path = os.path.join(BASE_DIR, "media/images/ts/webserver", "1.png")
        #
        # with open(img_path, 'rb') as f:
        #     base64_data = base64.b64encode(f.read())  # base64编码
        #     base64_str = str(base64_data, 'utf-8')
        #     print(base64_str)
        #
        # if len(base64_str) % 3 == 1:
        #     base64_str += "=="
        # elif len(base64_str) % 3 == 2:
        #     base64_str += "="
        # todo 注释上面
        base64_b = bytes(base64_str, encoding='utf8')
        img_data = base64.b64decode(base64_b)
        file_name = f"{uuid.uuid4()}.jpeg"
        file_path = "media/images/ts/webserver/" + file_name
        if not os.path.exists(os.path.join(BASE_DIR, "media/images/ts/webserver")):
            os.makedirs(os.path.join(BASE_DIR, "media/images/ts/webserver"))
        full_file_path = os.path.join(BASE_DIR, file_path)
        if os.path.exists(file_path):
            os.remove(full_file_path)  # 删除已存在的文件
        with open(full_file_path, 'wb') as f:
            f.write(img_data)
    except Exception as e:
        print(str(e))
    return file_path


if __name__ == '__main__':
    data_v1 = {
        "target": "127.0.0.1",
        "assets": [
            [
                "22",
                "ssh"
            ],
            [
                "80",
                "http"
            ]
        ],
        "assetinfo": {
            "http": [
                {
                    "port": "80",  # 端口号
                    "service": "http",  # 服务
                    "protocol": "tcp",  # 协议
                    "title": "Apache2 Ubuntu Default Page: It works",  # web服务标题
                    "finger": {
                        "middleware": [
                            {
                                "type": "middleware",  # 中间件类型
                                "name": "Ubuntu "  # 中间件名称
                            },
                            {
                                "type": "middleware",  # 中间件类型
                                "name": " Apache"  # 中间件名称
                            }
                        ],  # 中间件
                        "fingers": [
                            {
                                "type": "middleware",  # 中间件类型
                                "name": "Ubuntu "  # 中间件名称
                            }
                        ]  # web指纹
                    },  # 指纹识别
                    "dirs": [
                        [
                            "200",
                            "56B",
                            "/robots.txt"
                        ],
                        [
                            "204",
                            "201MB",
                            "/index.html"
                        ]
                    ]
                }
            ],  # HTTP服务的
            "weakpass": [
                {
                    "protocol": "ssh",  # 协议
                    "port": "22",  # 端口号
                    "ip": "127.0.0.1",  # ip地址
                    "user": "fengxuan",  # 用户名
                    "pass": "123480"  # 密码
                }
            ],  # 弱口令
            "vul": [
                {
                    "port": "80",  # 端口号
                    "name": "CVE-2018-3191",  # 漏洞名称
                    "cve_id": "CVE-2018-3191",  # CVE编号
                    "scan_time": "2022-12-12 01:01"  # 扫描时间
                }
            ]  # 漏洞
        }  # 资产详情
    }
    data_v2 = {
        "target": "1111",
        "assets": [
            {
                "port": 58000,
                "service": "http"
            },
            {
                "port": 22,
                "service": "ssh"
            }
        ],
        "assetinfo": {
            "http": [
                {
                    "port": 58000,
                    "service": "http",
                    "protocol": "tcp",
                    "title": "é»\u0098è®¤ç«\u0099ç\u0082¹ï¼\u0081",
                    "finger": {
                        "middleware": [
                            {
                                "type": "middleware",
                                "name": "Nginx"
                            }
                        ],
                        "fingers": []
                    },
                    "dirs": [],
                    "phpmyadmin": {},
                    "scan_time": "2022-04-29 10:31:46"
                }
            ],
            "weakpass": [],
            "vul": [
                {
                    "url": " http://124.221.154.4:58000 ",
                    "name": " XXXX SQL注入漏洞 PoC ",
                    "cve_id": "",
                    "component": "   Drupal  ",
                    "version": "   7.x   ",
                    "status": " success ",
                    "scan_time": "2022-04-29 10:33:39"
                }
            ]
        }
    }
    # data_v3 = {"task_id": "e1e4c5ac-f4ea-4c3f-a5cd-ecb4aa621b60", "status": 1, "msg": "TideFinger，PHPmyadmin扫描完成",
    #            "data": {"scan_time": "2022-05-25 09:12:08", "target": "171.84.0.27",
    #                     "assets": [{"port": "80", "service": "http"}], "assetinfo": {"http": [
    #                    {"port": "80", "service": "http", "protocol": "tcp", "title": "Index of /",
    #                     "finger": {"middleware": [{"type": "middleware", "name": "Nginx"}], "fingers": []},
    #                     "dirs": [["200", "25B", "/robots.txt"]], "phpmyadmin": {},
    #                     "screenshot_base64": "iVBORw0KGgoAAAANSUhEUgAAAyAAAAJYCAYAAACadoJwAAAAAXNSR0IArs4c6QAAIABJREFUeJzs3XlcVOX+B/DPsG/KCMMmGkgoKmpmLhW4lbnvJqbgkpa7XdPU0Cy7uWT9TC0yc7fcSk1BXDKXTM1MExNTu2IXxQVCYYCBAYaZ7++PuY6eBmVwIdPP+/XiFefZz8wk5zvPec6jEhEBERERERFRBbD7uwdARERERESPDgYgRERERERUYRiAEBERERFRhWEAQkREREREFYYBCBERERERVRgGIEREREREVGEYgBARERERUYVhAEJERERERBWGAQgREREREVUYBiBERERERFRhGIAQEREREVGFYQBCREREREQVhgEIERERERFVGAYgRERERERUYf7xAYharYZKpbL6uXr16t89tAplMpnwxRdfoF27dvD19YWDgwMcHR1RrVo1nDx58u8eHhERERERABsDEI1GU+pF/l9/VqxYcb/Ha+XEiRMYMmRIhff7ICksLETbtm0xcOBA7Ny5E5mZmWjUqBGqVauGS5cuQafT3VG7Z8+ehUqlgrOzM7Kzs+/xqImIiIjoUeRgS6GdO3fi5MmT+P7777F8+XJFXmhoKEaNGoXatWvj6aefvi+DvJ3HHnsM9erVq/B+HySxsbHYvXu35bhz587YsmULMjIyEBAQcMftrlmzBgDQvn17VKlS5a7HSURERERkUwDSqFEjNGrUCCEhIVYBSHh4OMaOHXtfBkdlKywsxKJFixRpL730EgDAz88PcXFxqF69+h21vXbtWgBA3759726QRERERET/Y1MAQg+uEydOoKCgQJH22GOPWX4fOXLkHbV77Ngx/P7773B3d0fXrl3vaoxERERERNf94xehA4BKpfq7h/C3uXbtmlWao6PjXbd7ffajW7ducHNzu+v2iIiIiIiAhyQAcXJy+ruH8LcpKSm5522KCL766isAvP2KiIiIiO6t+xKAxMTElPqUrN9//x0bN25E27ZtUaVKFahUKri5uaFBgwaYPn36bS+m09PTERsbi4YNG0KtVsPJyQk+Pj5o1qwZVq1aZdO4jEYjVq5ciY4dOyIgIABOTk6oVKkSGjVqhGnTpiEnJ8dSdteuXbd94tfo0aMBAGPHjrXKmzdvXrlfszNnzmDMmDGoV6+e5fz8/f3Rrl07LFy4EMXFxYryu3btQrt27dCnTx+rtp555hnLWI4ePVrusezfvx9paWnw8vJCu3btyl2fiIiIiOhW7ssakI8++gj169fHm2++qUiPiIhAcXExqlevDoPBAADQ6/VITk5GcnIyLl26hM8++8yqvW3btqFPnz6Wx8na29ujU6dO8PPzQ0ZGBg4fPlzmmK5du4YuXbrg0KFDAABfX18MGjQIW7duRVJSEpKSkrBmzRocOnQI3t7eaNWqFfbt24fXX38dx44dU7S1bNky9OjRAwDw7rvvonLlynjvvffg5+eHlStXokWLFuV6vebOnYs33ngDJpMJAPD888/jsccew4YNG7Bz507s3LkTCxYswPbt2xEYGAgA0Ol0qF69Opo3b46dO3cq2uvatSt8fHwAwPLf8rj+9KsXX3zxntzORURERERkIeWwf/9+AaD46datW6lljxw5YlX2/fffF4PBICIi2dnZ0rBhQ0W+vb29ZGRkKNo5efKkODk5Kcpt3LhRUWbu3LlWfWVmZirKdOrUSZF/5MgRERHZvXu3In3IkCGKer/++qs4ODgoygwfPtySf+XKFalevbo4OzvLoUOHyvNyiojIN998c8vXc9euXYq8p59+WkpKShT1t2zZYnXudzKO6wwGg3h7ewsA2bt37x23Q0RERERUmgpdAxIWFgYHB/Oki1qtxqRJkxT5RqPRarYhNjZWcftRmzZt0LNnz3L1++OPP2Lr1q2W4+DgYDRu3BgAEBkZqVjEvnr1ahQWFlqOGzRogPHjxyva+/zzz3HgwAEUFhaie/fuSEtLw5IlS+5oH5TY2FjF8YABAyy/P//886hRo4bl+KeffkJ8fHy5+yiPb7/9FteuXUNgYGC5Z3KIiIiIiMryty5Cr1WrllXazeswsrOzsX37dkV+9+7dy93P+vXrFcdBQUGW352cnODh4WE5LiwsxPHjxxXl33nnHTz++OOWYxHB0KFD8fLLL+Pw4cOIjY1FTExMucf166+/4vfff1ekhYWFKY7r16+vOF63bl25+ymP60+/6tOnD+zsHopnFBARERHRA+RvvcIs7elVImL5/ejRo1YL0+9k1/NffvlFcezu7q44dnZ2VhxfvnxZcezq6oqFCxcq0k6fPo1169ahe/fumDFjRrnHBMBqtgcAvL29Fce+vr6K4yNHjtxRX7YoKCiwzLDw6VdEREREdD880F9xnz9/3irNz8+v3O2kp6crjrdt26Z4atXVq1cV+dcXu9+sTZs26N+/v1X6lClT7ngfkitXrlilubq6Ko7/GiyVVude2bJlC3Q6HWrWrGm5RY2IiIiI6F56oHdCLy0QuJM9P/66U3hQUBBatWp1y/IhISGlpn/00UfYtm2bYvO/119/HT/88MMdBSF/HRdgfsLX7Y6LiopQUlJiWUtzL11/+hVnP4iIiIjofnmgA5C/zgYAUCwQt9VfZxEaNGiAFStWlLsdk8kENzc3RQBy4MABfP755xg+fPhdjwswL8S/3bGzs/N9CT60Wi127NgBgAEIEREREd0/D/QtWH9d/wAAGRkZ5W7n+t4Z15U281CW4uJi9OjRA2lpaYoF6QDw5ptvWq0bsUXVqlWt0vR6veL4r7NApdW5FzZs2IDi4mI8+eSTqF279n3pg4iIiIjogQ5AnnzySau0EydOlLudp556SnF89uzZcrcxdOhQ/Pjjj4iNjcV3330HNzc3S15OTo5lZ/S7GRcAq/Uofw24SqtzL1x/+hVnP4iIiIjofnqgA5Dg4GA88cQTirRNmzaVu52XXnpJcXzhwgXs3r3b5vqzZ8/GypUr0aNHD8yYMQM1atTAtGnTrMZV3rHVq1cPdevWVaSdOXNGcZycnKw47t27d7n6sMWVK1fw/fffQ6VSoU+fPve8fSIiIiKi6x7oAAQA3n77bcXxvn37sHz5cstxYWGh1V4af/XUU08hKipKkda3b198/fXXijUl165dw969exWP/k1ISMDkyZPx5JNP4ssvv7QsNh83bpzVDM3o0aMV+5jYYubMmYrjL7/80vL7d999p3gSWJMmTdCrV69ytW+Lr776CiaTCZGRkXjsscfueftERERERNfZFIAcOXIEX3zxBZYtW2aVd+rUKcybNw/bt29HdnY2ACAzMxN79uyxKnvw4EHLLUW5ubmllvnxxx+RmppqOe7ZsyfeeecdRZnBgwejQYMGaNy4MXx9fa326ACAiRMnYt++fZbjJUuWoEOHDpbjzMxM9OnTB25ublCr1XB0dIRGo0G7du1QXFyM3NxcbN26FdHR0RARTJw4UbH4+9q1a+jSpYuiz8uXL2PYsGH47bffrMZzK926dcOHH35o2fQvISEBbdq0weDBgxXBxhNPPIFNmzYpnop19uxZxTlet3XrVhw4cMDyfpSFT78iIiIiogojNvD29hYAZf4sX75cRESio6NvWaZPnz4iIvLee+/dsswTTzxhNYZDhw5J//79JTg4WFxcXASAODo6SqNGjWTu3LmlttOtWzerdhISEqRPnz4SHBwsbm5u4uTkJAEBAdK2bVuZNWuWXLhwQUREBg4ceMvzExGJiIi47WuRmZlpy0trceLECXn11VelVq1a4u7ubhlXx44dZenSpWIwGKzqBAYG3nYMQ4YMKbPflJQUASAODg7lHjMRERERUXmpRG7aepyIiIiIiOg+euDXgBARERER0cODAQgREREREVUYBiBERERERFRhGIAQEREREVGFYQBCREREREQVhgEIERERERFVGAYgRERERERUYRiAEBERERFRhWEAQkREREREFYYBCBERERERVRgGIEREREREVGEYgBARERERUYVhAEJERERERBWGAQgREREREVUYBiBERERERFRhGIAQEREREVGFYQBCREREREQVhgEIERERERFVGAYgRERERERUYRiAEBERERFRhWEAQkREREREFYYBCBERERERVRgGIEREREREVGEYgBARERERUYVhAEJERERERBWGAQgREREREVUYBiBERERERFRhGIAQEREREVGFcSirwOLFiytiHERERERE9A8XHByMF1544bZlygxAgoKC0KRJk3s2KCIiIiIienSpRET+7kEQEREREdGjgWtAiIiIiIiowjAAISIiIiKiCsMAhIiIiIiIKgwDECIiIiIiqjAMQIiIiIiIqMIwACEiIiIiogrDAISIiIiIiCoMAxAiIiIiIqowDECIiIiIiKjCMAAhIiIiIqIKwwCEiIiIiIgqDAMQIiIiIiKqMAxAiIiIiIiowjAAISIiIiKiClPhAUhJCRAenoPvviup6K6JiIiIiOhvVuEByKefFuHxx+3xwgsOFd01ERERERH9zVQiIhXV2dWrgnr1cnDgQGWEhvLuLyIiIiKiR02FBiDDhxegUiUVPvzQtaK6JCIiIiKiB0iF3Qf1669GJCQU48wZz4rqkoiIiIiIHjAVdh/Uv/5VgH//2xWVK6sqqksiIiIiInrAVEgAsn59MXJzBYMHO1dEd0RERERE9IAqVwDSqlUeXnutoNS8zExBtWparF1brEgvLAQmTtRj/nw32HHdORERERHRI61cIUF6uglZWaWvWTcagUuXBPn5yvwPPihE06YOaN6c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AGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1hAgAAAAAKwhQAAAAABYQ4AAAAAAsIYAAQAAAGANAQIAAADAGgIEAAAAgDUECAAAAABrCBAAAAAA1vx/+b0Pl4xtBPUAAAAASUVORK5CYII=",
    #                     "status": 200, "scan_time": "2022-05-25 09:13:37"}], "weakpass": [], "vul": []}}}
    #
    data_v4 = {"task_id": "06306bdd-6a0f-4b97-ab44-91eea2f0677a", "status": 1, "msg": "nmap扫描完成",
               "data": {"scan_time": "2022-05-26 09:04:31", "target": "171.84.0.27", "assets": [],
                        "assetinfo": {"http": [], "weakpass": [
                            {"protocol": "redis", "ip": "117.33.255.178:6379", "user": "None", "pass": "空",
                             "scan_time": "2022-05-27 15:47:30"}], "vul": []}}}
    parse(data_v4['data'])
    # print(67108864/1024/1024)
    # a = save_screenshot("1")
    # print(a)

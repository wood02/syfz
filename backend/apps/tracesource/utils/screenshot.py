# -*- coding: utf-8 -*-
import base64
import os
import time
from uuid import uuid4

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


def get_screenshot(url):
    try:
        # 设置浏览器
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')  # 无头参数
        options.add_argument('--disable-gpu')
        # 启动浏览器
        if os.getenv("DOCKERIZED"):
            driver = Chrome(executable_path='./chromedriver', options=options)
        else:
            driver = Chrome(executable_path='/Users/w_ood/Work/PythonStudy/workspce/motanni_workspace/syfz/backend/chromedriver', options=options)
        driver.implicitly_wait(5)
        # 访问目标URL
        driver.get(url)  # 使用get()方法，打开指定页面。注意这里是phantomjs是无界面的，所以不会有任何页面显示
        time.sleep(2)

        width = driver.execute_script("return document.documentElement.scrollWidth")
        height = driver.execute_script("return document.documentElement.scrollHeight")
        driver.set_window_size(width, height)  # 修改浏览器窗口大小
        pic_name = uuid4().urn[9:] + '.png'
        driver.get_screenshot_as_file(pic_name)  # 使用save_screenshot将浏览器正文部分截图，即使正文本分无法一页显示完全，save_screenshot也可以完全截图
        driver.close()  # 关闭phantomjs浏览器，不要忽略了这一步，否则你会在任务浏览器中发现许多phantomjs进程
        with open(pic_name, "rb") as f:
            # b64encode是编码，b64decode是解码
            screenshot = str(base64.b64encode(f.read()), encoding='utf-8')
    except Exception as e:
        screenshot = ''
        print(e)
    return screenshot


if __name__ == '__main__':
    url = 'https://www.baidu.com'
    get_screenshot(url)

# encoding:utf-8
import asyncio
import importlib
import json
import os
import warnings
from Syfz.settings import BASE_DIR
from apps.plugins.utils.file import File


class Verify:
    def __init__(self, app_dir, request_data):
        self.app_dir = app_dir
        self.request_data = request_data
        self.app_path = os.path.join(BASE_DIR, 'toolset')
        self.errors = []

    def get_app(self):
        dir_list = File.find_apps(path=self.app_path)
        if self.app_dir not in dir_list:
            return False
        return True

    def find_app_json(self):
        app_json = File.find_app_json(path=self.app_path, app_dir=self.app_dir)
        app_d = json.loads(app_json)
        return app_d

    def err(self):
        err_num = 0
        err_dict = {
            "app_name": "应用名称不存在",
            "action": "动作不存在",
            "params": "参数不存在",
        }
        err_data = []
        standard_args = self.find_app_json()['args'].get(self.request_data['action'], "")  # 标准所有数据
        if not standard_args:
            print("---", standard_args)
        args = self.request_data['args']  # 前端数据

        for arg in standard_args:
            key = arg['key']
            type = arg['type']
            required = arg['required']
            if required:  # 如果是必填的
                if key not in args.keys():  # 先判断是否有这个key
                    err_num += 1
                    err_data.append({key: "该字段为必填项！"})
                else:  # 有在判断是否满足要求
                    value = args.get(key)  # 根据key拿到前端数据 一个个验证
                    if type != "select":
                        if not isinstance(value, self.get_type(type)):  # 数据类型是否满足
                            err_num += 1
                            err_data.append({key: "数据类型错误！"})
                    else:
                        if value not in arg['data']:
                            err_num += 1
                            err_data.append({key: "数据选择错误！"})
            else:
                args[key] = ""
        self.request_data = args
        self.errors = err_data

    def is_valid(self):
        """
        整体进行验证
        :return:
        """
        if self.get_app():

            self.err()
            if not self.errors:
                return True

        return False

    def get_type(self, type):

        """
        验证类型
        :param type:
        :return:
        """

        if type in ["text", "password", "textarea"]:
            return str
        elif type == "number":
            return int, float


async def run_app(request_data):
    """
    执行函数 app函数
    :param request_data:
    :return:
    """
    try:
        # 导入模块
        expr_module = importlib.import_module(f"toolset.{request_data['app_dir']}.main.run", )
        args = request_data['args']
        # 获取模块的方法
        expr_func = getattr(expr_module, request_data['action'])
        warnings.simplefilter("ignore", RuntimeWarning)
        result = await expr_func(**args)
        print(result)
        return result
    except Exception as e:
        print("错误:", e)
        return {"status": 2, "result": [], "message": str(e)}


def run(request_data):
    """
    执行函数
    :param request_data:
    :return:
    """
    # 加入异步队列

    # There is no current event loop in thread 'Thread-1'.
    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)

    # 启动执行
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(run_app(request_data))  # 获取结果
    return result


if __name__ == '__main__':
    # redis
    """
     request_data = {
        "app_dir": "redis",
        "action": "get",
        "args": {
            "host": "localhost",
            "db": 8,
            "port": 6379,
            "key": "syfz_toolset_resis_test",
            "password": "",

        }
    }
    v = Verify(request_data['app_dir'], request_data)
    a = v.is_valid()
    print(a)
    print(v.errors)
    run(request_data)
    """

    # 测试app

    request_data = {
        "app_dir": "subdomain",
        "action": "subdomain",
        "args": {
            # "query": "sgcc.com.cn",

        }
    }
    v = Verify(request_data['app_dir'], request_data)
    a = v.is_valid()
    print(a)
    print(v.errors)
    run(request_data)

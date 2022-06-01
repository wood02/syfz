# encoding:utf-8
import asyncio
import importlib
import json
import os
import warnings
import validators
from loguru import logger

from Syfz.settings import BASE_DIR
from apps.plugins.utils.file import File
# from common.current.log import get_logger
# self.get_logger = get_logger("toolset", 'toolset.log', filter=lambda record: "toolset" in record["extra"])
# self.logger = self.get_logger.bind(toolset=True)
from common.utils import check_ip, check_domian


class Verify:
    def __init__(self, app_name, request_data):
        self.app_name = app_name
        self.request_data = request_data
        self.app_path = os.path.join(BASE_DIR, 'toolset')

        self.errors = {
            "app_name": "",
            "action": "",
            "params": [],
        }

    def get_app(self):
        dir_list = File.find_apps(path=self.app_path)
        if self.app_name not in dir_list:
            return False, f"{self.app_name}不存在"
        return True, "验证成功"

    def find_app_json(self):
        app_json = File.find_app_json(path=self.app_path, app_name=self.app_name)
        app_d = json.loads(app_json)
        return app_d

    def err(self):
        err_num = 0
        err_dict = self.errors
        logger.info(f"前端请求数据:{self.request_data}")

        standard_args = self.find_app_json()['args'].get(self.request_data['action'], "")  # 标准所有数据
        if not standard_args and standard_args != {}:
            err_dict['action'] = "动作不存在"

        args = self.request_data['args']  # 前端数据

        keys = []
        for arg in standard_args:
            key = arg['key']
            keys.append(key)  # 标准数据的key
            type = arg['type']
            required = arg['required']
            value = args.get(key, arg.get('default', ""))  # 根据key拿到前端数据 一个个验证 或者使用默认
            if required:  # 如果是必填的
                if key not in args.keys():  # 先判断是否有这个key
                    err_num += 1
                    err_dict['params'].append({key: "该字段为必填项！"})
            else:
                args[key] = value  # 如果不是必填的，则把默认值赋
            # 是不是必填都得验证
            if type != "select":
                val, msg = self.val_type(value, type)
                if not val:  # 数据类型是否满足
                    err_num += 1
                    err_dict['params'].append({key: msg})
            else:
                if value not in arg['data']:
                    err_num += 1
                    err_dict['params'].append({key: "数据选择错误！"})
        [args.pop(i) for i in list(args.keys()) if i not in keys]  # 删除前端数据中有标准数据中没有的数据
        self.request_data = args
        logger.info(f"APP运行参数数据:{self.request_data}")

    def is_valid(self):
        """
        整体进行验证
        :return:
        """
        app_success, msg = self.get_app()
        if app_success:
            self.err()
            for v in self.errors.values():
                if v:
                    return False
            return True
        else:
            self.errors["app_name"] = msg
        return False

    def val_type(self, value, type):

        """
        验证类型
        :param value: 要验证数据
        :param type: 类型
        :return:
        """
        # 导入模块
        expr_module = importlib.import_module(f"apps.plugins.utils.verify_type", )
        # 获取模块的方法
        if hasattr(expr_module, type):
            return getattr(expr_module, type)(value)
        else:
            return False, "类型错误"


async def run_app(request_data):
    """
    执行函数 app函数
    :param request_data:
    :return:
    """
    # todo 加上执行异常
    # try:
    # 导入模块
    expr_module = importlib.import_module(f"toolset.{request_data['app_name']}.main.run", )
    args = request_data['args']
    # 获取模块的方法
    expr_func = getattr(expr_module, request_data['action'])
    warnings.simplefilter("ignore", RuntimeWarning)
    result = await expr_func(**args)
    logger.info(f"APP运行结果数据:{result}")

    return result
    # except Exception as e:
    #     print("错误:", e)
    #     return {"status": 2, "result": [], "message": str(e)}


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

    # request_data = {
    #     "app_name": "redis",
    #     "action": "get",
    #     "args": {
    #         "host": "localhost",
    #         "db": 8,
    #         "port": 6379,
    #         "key": "syfz_toolset_resis_test",
    #         "password": "",
    #
    #     }
    # }
    # v = Verify(request_data['app_name'], request_data)
    # a = v.is_valid()
    # print(a)
    # print(v.errors)
    # run(request_data)

    # 测试app

    request_data = {
        "app_name": "subdomain",
        "action": "subdomain",
        "args": {
            "query": "/sgcc.com.cn",
        }
    }
    request_data = {
        "app_name": "JSFinder",
        "action": "search",
        "args": {
            "url": "httpssssss://103.45.116.194/"
        }
    }
    v = Verify(request_data['app_name'], request_data)
    a = v.is_valid()

    if a:
        print("验证是通过，无错误参数：", v.errors)
        print("执行结果：")
        run(request_data)
    else:
        print("验证失败：", v.errors)

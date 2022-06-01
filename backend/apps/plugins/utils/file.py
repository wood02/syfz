#!/usr/bin/env python
# encoding:utf-8
import os

no_path = ["__pycache__", "basic", "hide"]


class File():
    @staticmethod
    def find_apps(path):
        dir_list = []
        dir = os.listdir(path)
        dirs = [i for i in dir if os.path.isdir(os.path.join(path, i))]

        if dirs:
            for i in dirs:

                # 排查不需要的文件夹
                if i not in no_path:
                    dir_list.append(i)

        return dir_list

    @staticmethod
    def find_app_json(path, app_name):
        app_json = path + "/" + app_name + "/app.json"
        with open(app_json, 'rb') as f:
            return f.read()

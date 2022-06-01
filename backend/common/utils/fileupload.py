# -*- coding: utf-8 -*-
import os
from datetime import datetime

from common.drf.response import Response


class FileUpload:
    # 验证文件大小、扩展名、是不是日期文件夹
    def __init__(self, f_obj, ext, size=1024 * 1024, is_save=False, path=None, is_datefolder=False):
        self.f_obj = f_obj
        self.path = path
        self.ext = ext
        self.size = size
        self.is_save = is_save
        self.is_datefolder = is_datefolder

    def load(self):
        if not self.f_obj:
            return False, "请选择要上传文件"
        # 检测文件大小，上传文件的大小不能过大
        if not self.check_size():
            return False, "文件过大不能上传！"

        # 检测文件类型，必须是指定的几种文件扩展名对应的文件类型
        errors = {
            -1: '没有扩展名',
            -2: '无效的扩展名',
            -3: '未识别的扩展名',
            1: '有效的扩展名'
        }
        res = self.check_type()
        if res < 0:
            return False, errors[res]
        if self.is_save:
            # 获取文件路径
            file_path = self.get_path()

            # 上传文件
            if not self.write_file(file_path):
                return False, "文件读写错误"

        # 之前所有的检测都通过，才能返回True，否则返回对应的错误提示
        return True, self.f_obj

    def check_size(self):
        if self.f_obj.size > self.size:
            return False
        return True

    def check_type(self):
        ext = os.path.splitext(self.f_obj.name)

        if len(ext) <= 1:
            return -1

        ext = ext[1].lstrip('.')
        if isinstance(self.ext, str):
            if ext != self.ext:
                return -2
        elif isinstance(self.ext, (tuple, list)):
            if ext not in self.ext:
                return -2
        else:
            return -3
        return 1

    def get_path(self):
        if self.is_datefolder:
            folder_name = datetime.now().strftime('%Y/%m/%d')
            folder_path = os.path.join(self.path, folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            file_path = os.path.join(folder_path, self.f_obj.name)
        else:
            file_path = os.path.join(self.path, self.f_obj.name)
        return file_path

    def write_file(self, file_path):
        try:
            with open(file_path, 'wb') as fp:
                if self.f_obj.multiple_chunks():
                    for chip in self.f_obj.chunks():
                        fp.write(chip)
                else:
                    fp.write(self.f_obj.read())
            return True
        except:
            return False

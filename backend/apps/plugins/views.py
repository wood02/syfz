import json
import os.path
import shutil
import sys
import traceback
import codecs

from django.http import StreamingHttpResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView

from Syfz.settings import BASE_DIR
from apps.plugins.models import AppRunHistory
from apps.plugins.utils.file import File
from apps.plugins.utils.pages import Pagination
from apps.plugins.utils.verify import Verify, run
from apps.plugins.utils.zip import Zip
from common.drf.response import Response
from common.utils.fileupload import FileUpload

try:
    # try with a fast c-implementation ...
    import mmh3 as mmh3
except ImportError:
    # ... otherwise fallback to this code!
    import pymmh3 as mmh3


class ToolsetAPIView(APIView):
    # authentication_classes = []
    # permission_classes = []

    def get(self, request, format=None):
        # todo 做缓存 新增插件时，清空缓存 做个异常处理
        name = request.query_params.get('name', "")
        app_type = request.query_params.get('type', "")
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        if page <= 0:
            page = 1
        if page_size <= 0 or page_size > 100:
            page_size = 10
        # 获取插件列表
        app_data = []
        toolset_path = os.path.join(BASE_DIR, 'toolset')
        dir_list = File.find_apps(path=toolset_path)
        for d in dir_list:
            # 获取app.json
            try:
                app_json = File.find_app_json(path=toolset_path, app_name=d)
                app_d = json.loads(app_json)
                # app_d["app_dir"] = d
                # app_d["icon"] = d + "/icon.png"
                app_d["icon"] = d + "/icon.svg"

                if name or app_type:
                    if name in app_d['name'] and app_type in app_d['type']:
                        app_data.append({"app_name": d, "app_data": app_d})
                else:
                    app_data.append({"app_name": d, "app_data": app_d})
            except Exception as e:
                print("错误Toolset:", d, str(e))
        app_data = sorted(app_data, key=lambda x: x["app_data"]["order"], reverse=False)
        data = Pagination(data_list=app_data, page=page, page_size=page_size).show()
        return Response(success=True, data=data, message="success")


@api_view(["POST"])
def toolset_run(request, format=None):
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
    request_data = request.data
    arh = {
        "user": request.user,
        "app_name": request_data['app_name'],
        "request_data": request_data,
        "response_data": {},
        "status": 1,
    }
    # try:

    v = Verify(request_data['app_name'], request_data)
    # 存储运行记录

    if v.is_valid():
        # 验证成功
        response_data = run(request_data)
        arh['response_data'] = response_data
        AppRunHistory.objects.create(**arh)
        return Response(success=True, data=response_data, message='success')
    else:
        response_data = {"errors": v.errors}
        arh['status'] = 0
        arh['response_data'] = response_data
        AppRunHistory.objects.create(**arh)
        return Response(success=False, data=response_data, message='fail')
    # except Exception as e:
    #     _, _, exc_tb = sys.exc_info()
    #     error_msg = ""
    #     for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
    #         # print(filename, linenum, funcname, source)
    #         error_msg += "%-23s:%s '%s' in %s()\n" % (
    #             filename.replace(str(BASE_DIR) + "/", ""), linenum, source, funcname)
    #     arh['status'] = 2
    #     arh['error_msg'] = traceback.format_exc()
    #     arh['error_msg'] = error_msg
    #     AppRunHistory.objects.create(**arh)
    #     return Response(success=False, data=[], message='APP运行错误')


@api_view(["POST"])
def toolset_import(request, format=None):
    file = request.FILES.get('file')  # 前台读取到 name='file'

    filename = file.name

    if filename.split('.')[-1] == "zip":
        tmp_dir = os.path.join(BASE_DIR, 'tmp')
        app_dir = os.path.join(BASE_DIR, 'toolset')
        # 临时存放
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)

        file_path = tmp_dir + "/" + filename
        f = open(file_path, 'wb')
        for chunk in file.chunks():  # 按快读取
            f.write(chunk)
        f.close()

        save_path = app_dir + "/" + filename.replace(".zip", "")

        if os.path.exists(save_path):
            return Response(success=False, data=[], message="APP 已经存在")

        status = Zip.save(zip_path=file_path, save_path=save_path)

        if status:
            shutil.rmtree(tmp_dir)
            return Response(success=True, message="已上传")
        else:
            shutil.rmtree(tmp_dir)
            return Response(success=False, data=[], message="APP 格式不正确 或 压缩文件损坏")
    else:
        return Response(success=False, data=[], message='上传文件非 ZIP 压缩文件')


@api_view(["GET"])
def markdown_file_download(request):
    # app_dir = request.data.get("app_name", "")
    app_dir = request.query_params.get("app_name", "")
    if not app_dir:
        return Response(success=False, data=[], message='参数错误')
    the_file_name = os.path.join(BASE_DIR, 'toolset', app_dir, "readme.md")
    if not os.path.exists(the_file_name):
        return Response(success=False, data=[], message='文件不存在')

    def file_iterator(file_name, chunk_size=512):
        with open(file_name, "rb") as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c  # 可迭代
                else:
                    break

    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = f'attachment;filename="readme.md"'
    return response


@api_view(["GET"])
def icon_file_download(request):
    # icon = request.data.get("icon", "")
    icon = request.query_params.get("icon", "")
    if not icon:
        return Response(success=False, data=[], message='参数错误')

    the_file_name = os.path.join(BASE_DIR, 'toolset', icon)
    if not os.path.exists(the_file_name):
        return Response(success=False, data=[], message='文件不存在')

    def file_iterator(file_name, chunk_size=512):
        with open(file_name, "rb") as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c  # 可迭代
                else:
                    break

    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = f'attachment;filename="{icon}"'
    return response


class ImageHashAPIView(APIView):
    """
    icon上传
    """
    # permission_classes = []
    parser_classes = [MultiPartParser]  # 接收这几类数据格式

    def post(self, request, *args, **kwargs):
        file = self.request.data.get('image')
        try:
            fu = FileUpload(f_obj=file, ext=['jpg', 'jpeg', 'bmp', 'png', 'gif', 'icon', 'ico'], size=1024 * 1024 * 3)

            b, f = fu.load()
            if not b:
                return Response(success=False, message=f)

            icon_hash = mmh3.hash(codecs.lookup('base64').encode(file.file.read())[0])
            # file_obj = file.file.read()
            # icon_md5 = hashlib.md5(file_obj).hexdigest()
            return Response(success=True,
                            data={
                                "image_hash": icon_hash,
                                "image_hash_query": f'image_hash="{icon_hash}"',
                                "icon_hash_query": f'icon_hash="{icon_hash}"',
                            },
                            message="上传成功")

        except Exception as e:
            return Response(success=False, message=str(e))

# 新建response.py文件
from rest_framework.response import Response as DrfResponse
from rest_framework.serializers import Serializer


class Response(DrfResponse):

    def __init__(self, data=None, status=200, code=None, success=None, message=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.

        Setting 'renderer' and 'media_type' will typically be deferred,
        For example being set automatically by the `APIView`.
        """
        super(DrfResponse, self).__init__(self, None, status=status)

        if isinstance(data, Serializer):
            message = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(message)
        if not code:
            code = 200 if success else 0
        if message:
            self.data = {"code": code, "success": success, "data": data or [], "message": message}
        else:
            self.data = {"code": code, "success": success, "data": data or []}
        # if not self.data['data']:
        #     self.data.pop("data")
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in headers.items():
                self[name] = value


class APIResponse(DrfResponse):
    def __init__(self, status=0, msg='ok', http_status=None, headers=None, exception=False, **kwargs):
        # 将外界传入的数据状态码、状态信息以及其他所有额外存储在kwargs中的信息，都格式化成data数据
        data = {
            'status': status,
            'msg': msg
        }
        # 在外界数据可以用result和results来存储
        if kwargs:
            data.update(kwargs)

        super().__init__(data=data, status=http_status, headers=headers, exception=exception)

# 使用：
# APIResponse() 代表就返回 {"status": 0, "msg": "ok"}

# APIResponse(result="结果") 代表返回 {"status": 0, "msg": "ok", "result": "结果"}

# APIResponse(status=1, msg='error', http_status=400, exception=True) 异常返回 {"status": 1, "msg": "error"}

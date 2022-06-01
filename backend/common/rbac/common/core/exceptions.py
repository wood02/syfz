from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # 先调用DRF默认的 exception_handler 方法, 对异常进行处理，
    # 如果处理成功，会返回一个`Response`类型的对象
    error_stencil = {'data': '', 'message': '', 'code': 500, 'success': False}
    response = exception_handler(exc, context)
    if response is None:
        # 项目出错了，但DRF框架对出错的异常没有处理,
        # 可以在此处对异常进行统一处理，比如：保存出错信息到日志文件
        view = context['view']  # 出错的视图
        error = '服务器内部错误, %s' % exc
        print('%s: %s' % (view, error))
        error_stencil['data'] = []
        error_stencil['message'] = error
        error_stencil['code'] = 500
        # return Response(error_stencil)
    else:
        error_stencil['data'] = []
        error_stencil['message'] = response.data['detail']
        error_stencil['code'] = response.status_code
        if response.status_code == 200:
            error_stencil['success'] = True

    # return response
    return Response(error_stencil)

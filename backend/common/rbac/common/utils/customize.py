def make_response(data=None, message="success", code=200):
    """
    自定义返回体
    :param data: 要返回的数据
    :param message: 要返回的信息
    :param code: 状态码
    :return: 组装好的消息体
    """

    resp = dict()
    resp['code'] = code
    resp['success'] = True if code == 200 else False
    resp['data'] = data
    resp['message'] = message
    return resp

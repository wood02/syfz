from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.views import exception_handler
from rest_framework.request import Request

from common.drf.response import Response


# from common.log.logging import get_logger

# logger = get_logger(__file__)


def custom_exception_handler(exc, context):
    response: Response = exception_handler(exc, context)
    request: Request = context["request"]
    if response:
        # result = {}
        # logger.debug(
        #     {
        #         "请求用户": str(request.user),
        #         "请求路径": request.path,
        #         "请求参数": dict(request.query_params),
        #         "请求方法": request.method,
        #         "请求数据": request.data,
        #         "响应信息": response.data,
        #     }
        # )

        response_data = response.data
        print(response_data)
        detail = response_data.get("detail")
        non_field_errors = response_data.get("non_field_errors")
        # 三类异常处理

        if detail:
            code = detail.code
            if code == "not_found":
                message = "未找到，或无权限！"
            elif code == "password_mismatch":
                message = "两次密码不一致！"
            else:
                message = detail
            return Response(success=False, message=message, status=status.HTTP_200_OK)
        elif non_field_errors:
            for error in non_field_errors:
                if error.code == "unique":
                    message = '请不要重复操作'
                    return Response(success=False, message=message, status=status.HTTP_200_OK)
            return Response({"message": non_field_errors[0]}, status=status.HTTP_400_BAD_REQUEST)
        else:
            errors = response_data.get('errors')
            if errors and errors[0].code == "password_mismatch":
                return Response(success=False, message="两次密码不一致！", status=status.HTTP_200_OK)

            for key, value in response_data.items():
                # message = key + " " + value[0]
                message = value[0]
                return Response(response_data, success=False, message=message, status=status.HTTP_200_OK)
            return Response(response_data, success=False, message="接口参数错误！", status=status.HTTP_200_OK)
    return response

from django.utils.encoding import smart_text
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
import jwt
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication
from rest_framework_jwt.authentication import jwt_decode_handler
from rest_framework_jwt.settings import api_settings

from apps.rbac.models import Users


class JWTAuthentication(BaseJSONWebTokenAuthentication):
    # 自定义认证类，重写authenticate方法
    def check_jwt_token(self, request):
        """对携带的token请求头进行验证"""
        auth = get_authorization_header(request).split()
        auth_header_prefix = api_settings.JWT_AUTH_HEADER_PREFIX.lower()
        if not auth:
            if api_settings.JWT_AUTH_COOKIE:
                return request.COOKIES.get(api_settings.JWT_AUTH_COOKIE)
            raise AuthenticationFailed('无法获取到包含token的请求头，请检查请求头')
        if smart_text(auth[0].lower()) != auth_header_prefix:
            raise AuthenticationFailed('无效的token，授权标头错误。')
        if len(auth) == 1:
            # msg = 'Invalid Authorization header. No credentials provided.'
            raise AuthenticationFailed('无效的token，凭据字符串为空。')
        elif len(auth) > 2:
            # msg = 'Invalid Authorization header. Credentials string, should not contain spaces.'
            raise AuthenticationFailed('无效的token，凭据字符串不应包含空格。')
        return auth[1]

    def authenticate(self, request):
        """对token进行验证"""
        jwt_value = self.check_jwt_token(request)
        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            raise AuthenticationFailed('token已过期。')
        except jwt.DecodeError:
            raise AuthenticationFailed('token解码错误。')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('不合法的token。')
        # 得到的user对象，应该是自己user表的user对象
        # payload内容:{'user_id': 3, 'username': 'zzt', 'user_secret': 'urn:uuid:e9fdec49-1728-4d41-87c5-12b9aef0a189'}
        user = Users.objects.filter(id=payload['user_id']).first()  # 此处应该是自建的user表
        if user is None:
            raise AuthenticationFailed('用户不存在或已被删除。')
        user_secret = payload['user_secret']
        if user.user_secret.urn != user_secret:
            raise AuthenticationFailed('用户已退出，请重新登录。')
        return user, jwt_value


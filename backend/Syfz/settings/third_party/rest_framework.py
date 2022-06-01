from rest_framework import ISO_8601



REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FileUploadParser',
    ],
    # 全局认证

    # 权限认证
    # 设置所有接口都需要被验证都需要被验证
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # jwt 要打开
    ],
    # 身份验证
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 默认的验证是按照验证列表从上到下的验证
        'common.drf.simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',

    ],

    'DEFAULT_CONTENT_NEGOTIATION_CLASS': 'rest_framework.negotiation.DefaultContentNegotiation',
    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',
    'DEFAULT_VERSIONING_CLASS': None,

    # 通用视图配置
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],

    # Schema
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.openapi.AutoSchema',

    # 可选限流级别
    'DEFAULT_THROTTLE_CLASSES': [
        # 限制所有匿名未认证用户，使用IP区分用户
        'common.drf.throttling.AnonRateThrottle',
        # 限制经过认证后的用户，使用User_id 来区分
        # 'common.drf.throttling.UserRateThrottle'

        # 自定义
        'common.drf.throttling.CustomRateThrottle'

    ],

    # 设置访问频率
    'DEFAULT_THROTTLE_RATES': {
        'anon': '20/min',  # 从上 自定义一分钟可以访问30次 30/min
        'custom': '300/min',  # 自定义一分钟可以访问30次 30/min
    },
    'NUM_PROXIES': None,

    # 修改全局默认分页
    'DEFAULT_PAGINATION_CLASS': 'common.drf.pagination.MyPageNumberPagination',
    # 默认分页
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 10,

    # 过滤
    'SEARCH_PARAM': 'search',
    'ORDERING_PARAM': 'ordering',

    # 版本
    'DEFAULT_VERSION': None,
    'ALLOWED_VERSIONS': None,
    'VERSION_PARAM': 'version',

    # 身份验证
    'UNAUTHENTICATED_USER': 'django.contrib.auth.models.AnonymousUser',
    'UNAUTHENTICATED_TOKEN': None,

    # 视图配置
    'VIEW_NAME_FUNCTION': 'rest_framework.views.get_view_name',
    'VIEW_DESCRIPTION_FUNCTION': 'rest_framework.views.get_view_description',

    # 异常处理
    'EXCEPTION_HANDLER': 'common.drf.exception_handler.custom_exception_handler',
    'NON_FIELD_ERRORS_KEY': 'errors',
    # 'NON_FIELD_ERRORS_KEY': 'non_field_errors',

    # 测试
    'TEST_REQUEST_RENDERER_CLASSES': [
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer'
    ],
    'TEST_REQUEST_DEFAULT_FORMAT': 'multipart',

    # 超链接配置
    'URL_FORMAT_OVERRIDE': 'format',
    'FORMAT_SUFFIX_KWARG': 'format',
    'URL_FIELD_NAME': 'url',

    # 输入和输出格式化
    'DATE_FORMAT': ISO_8601,
    'DATE_INPUT_FORMATS': [ISO_8601],

    # 'DATETIME_FORMAT': ISO_8601, 2019-10-25T09:41:28.598222
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DATETIME_INPUT_FORMATS': [ISO_8601],

    'TIME_FORMAT': ISO_8601,
    'TIME_INPUT_FORMATS': [ISO_8601, ],

    # 编码
    'UNICODE_JSON': True,
    'COMPACT_JSON': True,
    'STRICT_JSON': True,
    'COERCE_DECIMAL_TO_STRING': True,
    'UPLOADED_FILES_USE_URL': True,

    # 可视化API
    'HTML_SELECT_CUTOFF': 1000,
    'HTML_SELECT_CUTOFF_TEXT': "More than {count} items...",

    # Schemas
    'SCHEMA_COERCE_PATH_PK': True,
    'SCHEMA_COERCE_METHOD_NAMES': {
        'retrieve': 'read',
        'destroy': 'delete'
    },
}

# drf-extensions配置
REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 5,  # 缓存全局过期时间（60 * 10 表示10分钟）
    'DEFAULT_CACHE_ERRORS': False,
}

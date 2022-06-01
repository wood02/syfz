from corsheaders.defaults import default_headers

# 跨域增加忽略
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True

CORS_EXPOSE_HEADERS = [
    'content-disposition',
    'key'
    # 自定义响应key
]

# CORS_ORIGIN_WHITELIST = (
#     '0.0.0.0'
# )

# CORS_ALLOW_HEADERS = list(default_headers) + ['content-disposition']
# 默认可以使用的非标准请求头，需要使用自定义请求头时，就可以进行修改
CORS_ALLOW_HEADERS = (
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    'content-disposition',
    'x-token',
)
# 默认请求方法
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'PATCH',
    'POST',
    'PUT',
)

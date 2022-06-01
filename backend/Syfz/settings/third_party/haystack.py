# HAYSTACK_CONNECTIONS = {
#     'default': {
#         # 'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
#         'ENGINE': 'haystack.backends.elasticsearch5_backend.Elasticsearch5SearchEngine',  # 5.x引擎
#         # 'URL': 'http://47.114.129.62:9200/',  # 此处为elasticsearch运行的服务器ip地址，端口号固定为9200
#         'URL': 'http://127.0.0.1:9200/',  # 此处为elasticsearch运行的服务器ip地址，端口号固定为9200
#         # 'URL': 'http://192.168.8.127:9200/',  # 此处为elasticsearch运行的服务器ip地址，端口号固定为9200
#         'INDEX_NAME': 'hwtools_knowledge_loophole',  # 指定elasticsearch建立的索引库的名称
#     },
# }
# H_ENGINE = 'haystack.backends.elasticsearch5_backend.Elasticsearch5SearchEngine'


import os

from Syfz.settings import BASE_DIR

HAYSTACK_CONNECTIONS = {
    'default': {
        # 'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'ENGINE': 'common.drf.whoosh_cn_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),  # whoosh_index 文件夹不需要自己手动创建 会自动创建
    }
}

# 当添加、修改、删除数据时，自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
# 指定搜索结果每页的条数
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10

HAYSTACK_DEFAULT_OPERATOR = 'AND'
# ALTER USER 'root'@'%' IDENTIFIED BY 'bb656d9b32cfeba1' PASSWORD EXPIRE NEVER;
#  ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'bb656d9b32cfeba1';
HAYSTACK_DOCUMENT_FIELD = 'q'  # 后面的 都要改为q search_indexs.py ser templates

from django.urls import path, re_path

from apps.plugins import views
from apps.plugins.views import ImageHashAPIView

urlpatterns = [
    path('toolset/', views.ToolsetAPIView.as_view(), name='toolset'),
    path('toolset/import/', views.toolset_import, name='toolset_import'),
    path('toolset/markdown_download/', views.markdown_file_download, name='markdown_download'),
    path('toolset/icon_download/', views.icon_file_download, name='icon_file_download'),
    path('toolset/run/', views.toolset_run, name='toolset_run'),
    path('toolset/image_hash/', ImageHashAPIView.as_view(), name='image_hash'),

]

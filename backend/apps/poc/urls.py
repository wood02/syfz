from rest_framework.routers import DefaultRouter

from apps.poc.views import PocViewSet

app_name = 'poc'

router = DefaultRouter()
routers = {
    'poc': PocViewSet,

}

for key, value in routers.items():
    router.register(key, value)
urlpatterns = [

]

urlpatterns += router.urls

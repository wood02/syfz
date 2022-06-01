# -*- coding: utf-8 -*-
from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.alarm.views import attack, hacker, event, attack_detail, passive

router = DefaultRouter()
routers = {
    'attack': attack.AttackViewSet,
    'attack_details': attack.AttackDetailsViewSet,
    'attack_white': attack.AttackWhiteViewSet,
    # 'hacker': hacker.HackerViewSet,
    # 'evidence_image': hacker.EvidenceImageViewSet,
    # 'event_file': event.EventFileViewSet,
    # 'event': event.EventViewSet,
    'detail_domain': attack_detail.DetailDomainViewSet,
    'detail_tag_info': attack_detail.DetailTagInfoViewSet,
    'detail_location': attack_detail.DetailLocationViewSet,
    'passive_ftoken': passive.FofaTokenViewSet,
    'passive_xbtapikey': passive.XtbApiKeyViewSet,
    'passive_nsfocusapikey': passive.NsfocusApiKeyViewSet,
    'passive_zoomeyetoken': passive.ZeyeTokenViewSet,

}
# router.register("hacker/search", search_hacker.HackerSearchViewSet, basename="hacker-search")

for key, value in routers.items():
    router.register(key, value)
urlpatterns = [
    path('assetMapping/', attack_detail.DetailFofaAPIView.as_view(), name='fofa'),
    path('assetMappingZeye/', attack_detail.DetailZoomeyeAPIView.as_view(), name='zoomeye'),

]
urlpatterns += router.urls

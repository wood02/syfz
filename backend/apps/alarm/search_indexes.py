# -*- coding: utf-8 -*-
#
# search_indexes.py
#

from django.utils import timezone
from haystack import indexes

from apps.alarm.models import Hacker


class HackerIndex(indexes.SearchIndex, indexes.Indexable):
    q = indexes.CharField(document=True, use_template=True)

    name = indexes.CharField(model_attr="name", null=True)
    sex = indexes.IntegerField(model_attr="sex", null=True)
    age = indexes.IntegerField(model_attr="age", null=True)
    occupation = indexes.CharField(model_attr="occupation", null=True)
    native_place = indexes.CharField(model_attr="native_place", null=True)
    address = indexes.CharField(model_attr="address", null=True)
    network_id = indexes.CharField(model_attr="network_id", null=True)
    email = indexes.CharField(model_attr="email", null=True)
    qq = indexes.CharField(model_attr="qq", null=True)
    phone = indexes.CharField(model_attr="phone", null=True)
    id_number = indexes.CharField(model_attr="id_number", null=True)
    other_info = indexes.CharField(model_attr="other_info", null=True)
    photo_source = indexes.CharField(model_attr="photo_source", null=True)

    # 攻击设施
    fingerprint_info = indexes.CharField(model_attr="fingerprint_info", null=True)
    attack_ip = indexes.CharField(model_attr="attack_ip", null=True)
    attack_type = indexes.CharField(model_attr="attack_type", null=True)
    virus_sample = indexes.CharField(model_attr="virus_sample", null=True)
    domain = indexes.CharField(model_attr="domain", null=True)
    other_facilities = indexes.CharField(model_attr="other_facilities", null=True)

    def get_model(self):
        return Hacker

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

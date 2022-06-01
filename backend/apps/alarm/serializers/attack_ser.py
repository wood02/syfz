# -*- coding: utf-8 -*-
import datetime
import random

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from apps.alarm.conf import TASK_ADD
from apps.alarm.models import Attack, AttackDetails, AttackWhite
from apps.alarm.serializers.attack_detail_ser import DetailDomainSerializer, DetailTagInfoSerializer, \
    DetailLocationSerializer
from apps.alarm.serializers.hacker_ser import HackerSimpleListSerializer
from apps.alarm.serializers.event_ser import EventSimpleListSerializer

from common.utils.check_ip import check_ipv4_segment


class AttackDetailsSerializer(ModelSerializer):
    class Meta:
        model = AttackDetails
        exclude = ["created_at", "updated_at", "attack"]


class AttackSerializer(ModelSerializer):
    attack_details = AttackDetailsSerializer(many=True, required=False, allow_null=True)

    def validate_source_ip(self, source_ip):
        awe = AttackWhite.objects.filter(white_ip=source_ip).exists()
        if awe:
            raise ValidationError("已在白名单，添加失败！")
        return source_ip

    def create(self, validated_data):
        attack_details = []
        if validated_data.get("attack_details") or validated_data.get("attack_details") == []:
            attack_details = validated_data.pop('attack_details')

        attack, created = Attack.objects.get_or_create(source_ip=validated_data.get("source_ip"),
                                                       defaults=validated_data)
        # 如果没有创建则运行查询定时任务
        if created and TASK_ADD:
            # 58.218.208.13
            # todo 后台任务
            from apps.alarm.tasks import run_alarm_detail
            run_alarm_detail(attack.source_ip, attack.id)

        for detail in attack_details:
            # 最早时间
            attack_time = detail.get("attack_time")
            attack_earliest_time = attack.attack_earliest_time
            if not attack_earliest_time:
                # 如果最早时间不存在
                attack.attack_earliest_time = attack_time
                attack.save()
            else:

                if attack_time < attack.attack_earliest_time:
                    attack.attack_earliest_time = attack_time
                    attack.save()
            AttackDetails.objects.get_or_create(attack=attack, **detail)
        return attack

    class Meta:
        model = Attack
        exclude = ['fz_result_raw']
        extra_kwargs = {
            'trace_rate': {'read_only': True}
        }


class AttackUpdateSerializer(ModelSerializer):
    class Meta:
        model = Attack
        fields = ["fz_status"]
        # fields = ["hacker", "event"]


class AttackListSerializer(ModelSerializer):
    # hacker = HackerSimpleListSerializer()
    # event = EventSimpleListSerializer()
    attack_details = AttackDetailsSerializer(many=True)

    # detail_domain = DetailDomainSerializer(many=True)
    # detail_tag_info = DetailTagInfoSerializer(many=True)
    # detail_location = DetailLocationSerializer(many=True)

    def to_representation(self, instance):
        """to_representation自定义序列化数据的返回"""
        data = super().to_representation(instance)
        if instance.domain_num == 0:
            """
            更新之前老数据
            """
            domain_ins = instance.detail_domain.first() if instance.detail_domain else []
            domain_num = len(domain_ins.domain) if domain_ins else 0
            instance.domain_num = domain_num
            data.update(domain_num=domain_num)
            instance.save()
        # if instance.fz_start_time and instance.fz_status == 1 and instance.fz_task_id:
        #     if instance.fz_start_time + datetime.timedelta(minutes=60 * 2) <= datetime.datetime.now():
        #         fz_end_time = datetime.datetime.now() - datetime.timedelta(minutes=random.randint(0, 10))
        #         data['fz_status'] = 2
        #         data['fz_end_time'] = datetime.datetime.strftime(fz_end_time, '%Y-%m-%d %H:%M:%S')
        #         instance.fz_status = 2
        #         instance.fz_end_time = fz_end_time
        #         instance.save()

        return data

    class Meta:
        model = Attack
        exclude = ['hacker', 'event', 'fz_result_raw']
        # fields = "__all__"


class BatchAttackSerializer(ModelSerializer):
    """
    批量新增
    """

    # ips = serializers.ListSerializer()
    source_ip = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Attack
        fields = ["source_ip"]


class AttackWhiteSerializer(ModelSerializer):

    def validate_white_ip(self, white_ip):
        if not check_ipv4_segment(white_ip):
            raise ValidationError("ip格式错误！")
        if AttackWhite.objects.filter(white_ip=white_ip).exists():
            raise ValidationError("ip已经存在！")

        return white_ip

    class Meta:
        model = AttackWhite
        fields = "__all__"

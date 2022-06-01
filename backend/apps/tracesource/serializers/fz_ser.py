from rest_framework.serializers import ModelSerializer

from apps.tracesource.models.fz import ScanPort, WebServer, DirectoryBlast, Vulnerability, WeakPassword
from common.drf.serializers import DynamicFieldsModelSerializer


class ScanPortSerializer(DynamicFieldsModelSerializer):

    def create(self, validated_data):
        source_ip = validated_data.get("source_ip")
        sp, is_create = ScanPort.objects.update_or_create(source_ip=source_ip, defaults=validated_data)

        return sp

    class Meta:
        model = ScanPort
        exclude = ['raw_data']


class WebServerSerializer(DynamicFieldsModelSerializer):

    def create(self, validated_data):
        site = validated_data.get("site")
        ws, is_create = WebServer.objects.update_or_create(source_ip=site, defaults=validated_data)

        return ws

    class Meta:
        model = WebServer
        exclude = ['raw_data']


class DirectoryBlastSerializer(DynamicFieldsModelSerializer):

    def create(self, validated_data):
        source_ip = validated_data.get("source_ip")
        db, is_create = DirectoryBlast.objects.update_or_create(source_ip=source_ip, defaults=validated_data)

        return db

    class Meta:
        model = DirectoryBlast
        exclude = ['search_code_str', 'search_dir_str', 'raw_data']


class VulnerabilitySerializer(DynamicFieldsModelSerializer):

    def create(self, validated_data):
        source_ip = validated_data.get("source_ip")
        vul, is_create = Vulnerability.objects.update_or_create(source_ip=source_ip, defaults=validated_data)

        return vul

    class Meta:
        model = Vulnerability
        exclude = ['raw_data']


class WeakPasswordSerializer(DynamicFieldsModelSerializer):
    def create(self, validated_data):
        source_ip = validated_data.get("source_ip")
        wp, is_create = Vulnerability.objects.update_or_create(source_ip=source_ip, defaults=validated_data)

        return wp

    class Meta:
        model = WeakPassword
        exclude = ['raw_data']

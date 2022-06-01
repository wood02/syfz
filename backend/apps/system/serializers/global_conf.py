
from apps.system.models.global_conf import GlobalConfig
from common.drf.serializers import DynamicFieldsModelSerializer


class GlobalConfigSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = GlobalConfig
        fields = '__all__'

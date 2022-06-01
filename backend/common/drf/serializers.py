from rest_framework import serializers


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)  # 提取fields

        # 实例化父类
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # 删除fields参数中未指定的任何字段
            allowed = set(fields)
            existing = set(self.fields.keys())
            if allowed:
                for field_name in existing - allowed:
                    self.fields.pop(field_name)
            else:
                # fields参数为空，则取全部字段
                pass

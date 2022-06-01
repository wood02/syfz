import ipaddress
import re
from datetime import datetime


from rest_framework import serializers

from apps.poc.models import Poc


class PocListSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Poc
        fields = ('id', 'poc_id', 'poc_name', 'vulnerability', 'poc_desc', 'created_at', 'username')


class PocSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poc
        fields = '__all__'

    # 对数据做一些处理
    def to_internal_value(self, data):
        poc_id = data.get('poc_id', None)
        poc_name = data.get('poc_name', None)
        component = data.get('component', None)
        version = data.get('version', None)
        poc_desc = data.get('poc_desc', None)
        vulnerability = data.get('vulnerability', None)
        method = data.get('method', None)
        path = data.get('path', None)
        header = data.get('header', None)
        cookie = data.get('cookie', None)
        params = data.get('params', None)
        status_code = data.get('status_code', None)
        content = data.get('content', None)

        # poc_id
        if poc_id:
            rs = len(re.findall(r'\W', poc_id))
            if '_' in poc_id:
                rs += 1
            if rs == len(poc_id):
                raise serializers.ValidationError({"msg": 'poc_id不支持纯符号'})
        else:
            dt = datetime.now().strftime('%Y%m%d')
            pocs = Poc.objects.filter(poc_id__contains=dt).order_by('-poc_id').first()
            if pocs:
                poc_id = str(int(pocs.poc_id) + 1)
            else:
                poc_id = dt + '001'

            data['poc_id'] = poc_id

        #  PoC名称
        rs = len(re.findall(r'\W', poc_name))
        if '_' in poc_name:
            rs += 1
        if rs == len(poc_name) or poc_name.isdigit():
            raise serializers.ValidationError({"msg": 'PoC名称不支持纯符号、纯数字'})

        # 影响组件
        if component:
            rs = len(re.findall(r'\W', component))
            if '_' in component:
                rs += 1
            if rs == len(component) or component.isdigit():
                raise serializers.ValidationError({"msg": '影响组件不支持纯符号、纯数字'})
        # 影响版本
        if version:
            rs = len(re.findall(r'\W', version))
            if '_' in version:
                rs += 1
            if rs == len(version):
                raise serializers.ValidationError({"msg": '影响版本不支持纯符号'})

        # PoC描述
        if poc_desc:
            rs = len(re.findall(r'\W', poc_desc))
            if '_' in poc_desc:
                rs += 1
            if rs == len(poc_desc) or poc_desc.isdigit():
                raise serializers.ValidationError({"msg": 'PoC描述不支持纯符号、纯数字'})

        # 关联漏洞
        if vulnerability:
            rs = len(re.findall(r'\W', vulnerability))
            if '_' in vulnerability:
                rs += 1
            if rs == len(vulnerability):
                raise serializers.ValidationError({"msg": '关联漏洞不支持纯符号'})

        # 请求方式
        if method not in ('GET', 'POST', 'HEAD', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE'):
            raise serializers.ValidationError({"msg": '请正确输入请求方式'})

        # 路径
        if not path.startswith('/'):
            raise serializers.ValidationError({"msg": '路径必须以"/"开头'})

        # 请求头
        if header:
            rs = len(re.findall(r'\W', header))
            if '_' in header:
                rs += 1
            if rs == len(header) or header.isdigit():
                raise serializers.ValidationError({"msg": '请求头不支持纯符号、纯数字'})

        # 参数
        if params:
            for i in params:
                key = i.get('key')
                value = i.get('value')
                if key and value:
                    if not key.isalnum() or not value.isalnum():
                        raise serializers.ValidationError({"msg": '参数key或value只支持数字、字母、数字+字母组合'})
                elif not key and not value:
                    continue
                else:
                    raise serializers.ValidationError({"msg": '参数key或value要么同时存在要么同时不存在'})

        # cookie
        if cookie and not cookie.isalnum():
            raise serializers.ValidationError({"msg": 'cookie只支持数字、字母、数字+字母组合'})

        # 状态码
        if status_code and content:
            raise serializers.ValidationError({"msg": '状态码和匹配字只能选一个'})
        elif not status_code and not content:
            raise serializers.ValidationError({"msg": '状态码和匹配字两者必填一项'})
        elif status_code:
            rs = len(re.findall(r'\W', status_code))
            if '_' in status_code:
                rs += 1
            if rs == len(status_code):
                raise serializers.ValidationError({"msg": '状态码不支持纯符号'})
        elif content:
            rs = len(re.findall(r'\W', content))
            if '_' in content:
                rs += 1
            if rs == len(content) or content.isdigit():
                raise serializers.ValidationError({"msg": '内容匹配字不支持纯符号、纯数字'})

        ret = super(PocSerializer, self).to_internal_value(data)
        return ret

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     print(instance)
    #     # data["username"] = data.user.username
    #     return data



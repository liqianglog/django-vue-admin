from rest_framework import serializers

from apps.op_drf.serializers import CustomModelSerializer
from apps.system.models import DictData, DictDetails, ConfigSettings, SaveFile


# ================================================= #
# ************** 字典管理 序列化器  ************** #
# ================================================= #

class DictDataSerializer(CustomModelSerializer):
    """
    字典管理 简单序列化器
    """

    class Meta:
        model = DictData
        exclude = ('description', 'creator', 'modifier')


class ExportDictDataSerializer(CustomModelSerializer):
    """
    导出 字典管理 简单序列化器
    """

    class Meta:
        model = DictData
        fields = ('id', 'dictName', 'dictType', 'status', 'creator', 'modifier', 'remark',)


class DictDataCreateUpdateSerializer(CustomModelSerializer):
    """
    字典管理 创建/更新时的列化器
    """

    class Meta:
        model = DictData
        fields = '__all__'


# ================================================= #
# ************** 字典详情 序列化器  ************** #
# ================================================= #

class DictDetailsSerializer(CustomModelSerializer):
    """
    字典详情 简单序列化器
    """
    dictType = serializers.CharField(source='dict_data.dictType', default='', read_only=True)

    class Meta:
        model = DictDetails
        exclude = ('description', 'creator', 'modifier')


class ExportDictDetailsSerializer(CustomModelSerializer):
    """
    导出 字典详情 简单序列化器
    """

    class Meta:
        model = DictDetails
        fields = ('id', 'dictLabel', 'dictValue', 'is_default', 'status', 'sort', 'creator', 'modifier', 'remark',)


class DictDetailsListSerializer(CustomModelSerializer):
    """
    字典详情List 简单序列化器
    """

    class Meta:
        model = DictDetails
        fields = ('dictLabel', 'dictValue', 'is_default')


class DictDetailsCreateUpdateSerializer(CustomModelSerializer):
    """
    字典详情 创建/更新时的列化器
    """

    class Meta:
        model = DictDetails
        fields = '__all__'


# ================================================= #
# ************** 参数设置 序列化器  ************** #
# ================================================= #

class ConfigSettingsSerializer(CustomModelSerializer):
    """
    参数设置 简单序列化器
    """

    class Meta:
        model = ConfigSettings
        exclude = ('description', 'creator', 'modifier')


class ExportConfigSettingsSerializer(CustomModelSerializer):
    """
    导出 参数设置 简单序列化器
    """

    class Meta:
        model = ConfigSettings
        fields = (
        'id', 'configName', 'configKey', 'configValue', 'configType', 'status', 'creator', 'modifier', 'remark')


class ConfigSettingsCreateUpdateSerializer(CustomModelSerializer):
    """
    参数设置 创建/更新时的列化器
    """

    class Meta:
        model = ConfigSettings
        fields = '__all__'


# ================================================= #
# ************** 参数设置 序列化器  ************** #
# ================================================= #

class SaveFileSerializer(CustomModelSerializer):
    """
    文件管理 简单序列化器
    """
    file_url = serializers.CharField(source='file.url', read_only=True)

    class Meta:
        model = SaveFile
        exclude = ('description',)


class SaveFileCreateUpdateSerializer(CustomModelSerializer):
    """
    字典详情 创建/更新时的列化器
    """
    file_url = serializers.CharField(source='file.url', read_only=True)

    def save(self, **kwargs):
        files = self.context.get('request').FILES.get('file')
        self.validated_data['name'] = files.name
        self.validated_data['size'] = files.size
        self.validated_data['type'] = files.content_type
        self.validated_data['address'] = '本地存储'
        instance = super().save(**kwargs)
        # 进行判断是否需要OSS上传
        return instance

    class Meta:
        model = SaveFile
        fields = '__all__'

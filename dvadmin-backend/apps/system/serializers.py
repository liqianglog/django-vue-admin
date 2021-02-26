from rest_framework import serializers

from apps.op_drf.serializers import CustomModelSerializer
from apps.system.models import DictData, DictDetails


# ================================================= #
# ************** 字典管理 序列化器  ************** #
# ================================================= #

class DictDataSerializer(serializers.ModelSerializer):
    """
    字典管理 简单序列化器
    """

    class Meta:
        model = DictData
        exclude = ('description', 'creator', 'modifier')


class DictDataCreateUpdateSerializer(CustomModelSerializer):
    """
    字典管理 创建/更新时的列化器
    """

    class Meta:
        model = DictData
        exclude = ('description', 'creator', 'modifier')
        read_only_fields = ('update_datetime', 'create_datetime', 'creator', 'modifier')


# ================================================= #
# ************** 字典详情 序列化器  ************** #
# ================================================= #

class DictDetailsSerializer(serializers.ModelSerializer):
    """
    字典详情 简单序列化器
    """
    dictType = serializers.CharField(source='dict_data.dictType', default='', read_only=True)

    class Meta:
        model = DictDetails
        exclude = ('description', 'creator', 'modifier')

class DictDetailsListSerializer(serializers.ModelSerializer):
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
        exclude = ('description', 'creator', 'modifier')
        read_only_fields = ('update_datetime', 'create_datetime', 'creator', 'modifier')

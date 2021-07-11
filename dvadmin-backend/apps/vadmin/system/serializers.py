from django.core.cache import cache
from rest_framework import serializers

from application import settings
from apps.vadmin.op_drf.serializers import CustomModelSerializer
from apps.vadmin.system.models import DictData, DictDetails, ConfigSettings, SaveFile, MessagePush, MessagePushUser
from apps.vadmin.system.models import LoginInfor, OperationLog, CeleryLog


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

    def save(self, **kwargs):
        if getattr(settings, "REDIS_ENABLE", False):
            cache.delete('system_dict_details')
        return super().save(**kwargs)

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

    def save(self, **kwargs):
        if getattr(settings, "REDIS_ENABLE", False):
            cache.delete('system_configKey')
        return super().save(**kwargs)

    class Meta:
        model = ConfigSettings
        fields = '__all__'


# ================================================= #
# ************** 文件管理 序列化器  ************** #
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
    文件管理 创建/更新时的列化器
    """
    file_url = serializers.SerializerMethodField(read_only=True)

    def get_file_url(self, obj: SaveFile):
        return getattr(obj.file, "url", obj.file) if hasattr(obj, "file") else ""

    def save(self, **kwargs):
        files = self.context.get('request').FILES.get('file')
        self.validated_data['name'] = files.name
        self.validated_data['size'] = files.size
        self.validated_data['type'] = files.content_type
        self.validated_data['address'] = '本地存储'
        self.validated_data['source'] = '用户上传'
        instance = super().save(**kwargs)
        # 进行判断是否需要OSS上传
        return instance

    class Meta:
        model = SaveFile
        fields = '__all__'


# ================================================= #
# ************** 消息通知 序列化器  ************** #
# ================================================= #
class MessagePushSerializer(CustomModelSerializer):
    """
    消息通知 简单序列化器
    """

    class Meta:
        model = MessagePush
        fields = "__all__"

    def save(self, **kwargs):
        return super().save(**kwargs)


class MessagePushCreateUpdateSerializer(CustomModelSerializer):
    """
    消息通知 创建/更新时的列化器
    """

    class Meta:
        model = MessagePush
        fields = "__all__"


class ExportMessagePushSerializer(CustomModelSerializer):
    """
    导出 消息通知 简单序列化器
    """
    users = serializers.CharField(read_only=True)

    def get_users(self, obj):
        return ','.join(MessagePush.objects.filter(id=obj.id).values_list('user__username', flat=True))

    class Meta:
        model = MessagePush
        fields = (
            'id', 'title', 'content', 'message_type', 'is_reviewed', 'status', 'users', 'creator', 'modifier',
            'update_datetime', 'create_datetime')


class MessagePushUserSerializer(CustomModelSerializer):
    """
    消息通知 用户查询简单序列化器
    """
    # users = UserProfileSerializer(read_only=True)
    # users = serializers.SerializerMethodField(read_only=True)
    is_read = serializers.SerializerMethodField(read_only=True)

    # def get_users(self, obj):
    #     return UserProfileSerializer(obj.user.all(), many=True).data
    # 返回这个消息是否已读
    def get_is_read(self, obj):
        object = MessagePushUser.objects.filter(message_push=obj, user=self.context.get('request').user).first()
        return object.is_read if object else False

    class Meta:
        model = MessagePush
        fields = "__all__"

    def save(self, **kwargs):
        return super().save(**kwargs)


# ================================================= #
# ************** 登录日志 序列化器  ************** #
# ================================================= #

class LoginInforSerializer(CustomModelSerializer):
    """
    登录日志 简单序列化器
    """

    class Meta:
        model = LoginInfor
        fields = "__all__"


class ExportLoginInforSerializer(CustomModelSerializer):
    """
    导出 登录日志 简单序列化器
    """

    class Meta:
        model = LoginInfor
        fields = ('id', 'creator_name', 'ipaddr', 'loginLocation', 'browser', 'os',
                  'status', 'msg')


# ================================================= #
# ************** 操作日志 序列化器  ************** #
# ================================================= #

class OperationLogSerializer(CustomModelSerializer):
    """
    操作日志 简单序列化器
    """

    class Meta:
        model = OperationLog
        fields = "__all__"


class ExportOperationLogSerializer(CustomModelSerializer):
    """
    导出 操作日志 简单序列化器
    """

    class Meta:
        model = OperationLog
        fields = ('request_modular', 'request_path', 'request_body', 'request_method', 'request_msg', 'request_ip',
                  'request_browser', 'response_code', 'request_location', 'request_os', 'json_result', 'status',
                  'creator_name')


# ================================================= #
# ************** celery定时日志 序列化器  ************** #
# ================================================= #

class CeleryLogSerializer(CustomModelSerializer):
    """
    定时日志 简单序列化器
    """

    class Meta:
        model = CeleryLog
        fields = "__all__"


class ExportCeleryLogSerializer(CustomModelSerializer):
    """
    导出 定时日志 简单序列化器
    """

    class Meta:
        model = CeleryLog
        fields = ('name', 'kwargs', 'seconds', 'status', 'result', 'creator_name')

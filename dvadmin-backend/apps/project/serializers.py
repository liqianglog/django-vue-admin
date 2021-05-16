from rest_framework import serializers

from project.models import Project
from vadmin.op_drf.serializers import CustomModelSerializer


# ================================================= #
# ************** 项目管理 序列化器  ************** #
# ================================================= #
class ProjectSerializer(CustomModelSerializer):
    """
    项目管理 简单序列化器
    """

    class Meta:
        model = Project
        fields = '__all__'


class ProjectCreateUpdateSerializer(CustomModelSerializer):
    """
    项目管理 创建/更新时的列化器
    """

    # 此处可写定制的 创建/更新 内容
    def validate(self, attrs: dict):
        return super().validate(attrs)

    class Meta:
        model = Project
        fields = '__all__'


class ExportProjectSerializer(CustomModelSerializer):
    """
    导出 项目管理 简单序列化器
    """
    person__username = serializers.SerializerMethodField(read_only=False)
    dept__deptName = serializers.SerializerMethodField(read_only=False)

    def get_person__username(self, obj):
        return "" if not hasattr(obj, 'person') else obj.person.username

    def get_dept__deptName(self, obj):
        return "" if not hasattr(obj, 'dept') else obj.dept.deptName

    class Meta:
        model = Project
        fields = ('id', 'name', 'code', 'person', 'person__username', 'dept', 'dept__deptName', 'creator', 'modifier',
                  'description')

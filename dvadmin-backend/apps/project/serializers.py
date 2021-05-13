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
        exclude = ('description', 'creator', 'modifier')


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

    class Meta:
        model = Project
        fields = ('id', 'name', 'code', 'person__username', 'dept__deptName', 'creator', 'modifier', 'remark')

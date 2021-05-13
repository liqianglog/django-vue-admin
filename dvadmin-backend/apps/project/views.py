from project.filters import ProjectFilter
from project.models import Project
from project.serializers import ProjectSerializer, ProjectCreateUpdateSerializer, ExportProjectSerializer
from apps.vadmin.op_drf.filters import DataLevelPermissionsFilter
from apps.vadmin.op_drf.viewsets import CustomModelViewSet
from apps.vadmin.permission.permissions import CommonPermission


class ProjectModelViewSet(CustomModelViewSet):
    """
    项目管理 的CRUD视图
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer  # 序列化器
    create_serializer_class = ProjectCreateUpdateSerializer  # 创建/更新时的列化器
    update_serializer_class = ProjectCreateUpdateSerializer  # 创建/更新时的列化器
    filter_class = ProjectFilter  # 过滤器
    extra_filter_backends = [DataLevelPermissionsFilter]  # 数据权限类，不需要可注释掉
    update_extra_permission_classes = (CommonPermission,)  # 判断用户是否有这条数据的权限
    destroy_extra_permission_classes = (CommonPermission,)  # 判断用户是否有这条数据的权限
    create_extra_permission_classes = (CommonPermission,)  # 判断用户是否有这条数据的权限
    search_fields = ('name',)  # 搜索
    ordering = ['create_datetime']  # 默认排序
    # 导出
    export_field_data = ['项目序号', '项目名称', '项目编码', '项目负责人', '项目所属部门', '创建者', '修改者', '备注']  # 导出
    export_serializer_class = ExportProjectSerializer  # 导出序列化器
    # 导入
    import_field_data = {'name': '项目名称', 'code': '项目编码', 'person': '项目负责人ID', 'dept': '部门ID'}
    import_serializer_class = ExportProjectSerializer


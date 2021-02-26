import json

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.op_drf.viewsets import CustomModelViewSet
from apps.permission.filters import MenuFilter, DeptFilter, PostFilter, RoleFilter
from apps.permission.models import Role, Menu, Dept, Post
from apps.permission.serializers import UserProfileSerializer, MenuSerializer, RoleSerializer, \
    MenuCreateUpdateSerializer, DeptSerializer, DeptCreateUpdateSerializer, PostSerializer, PostCreateUpdateSerializer, \
    RoleCreateUpdateSerializer
from utils.response import SuccessResponse


class GetUserProfileView(APIView):
    """
    获取用户详细信息
    """

    def get(self, request, format=None):
        user_dict = UserProfileSerializer(request.user).data

        return SuccessResponse({
            'permissions': ["*:*:*"] if not user_dict.get('admin') else Menu.objects.filter(
                role__userprofile=request.user).values_list('perms', flat=True),
            # 'roles': Role.objects.filter(userprofile=request.user).values_list('roleKey', flat=True),
            'roles': ['admin'],
            'user': user_dict
        })


class GetRouters(APIView):
    """
    获取用户详细信息
    """

    def get(self, request, format=None):
        # data = GetUserInfoSerializer(request.user).data
        data = '{"msg":"操作成功","code":200,"data":[{"name":"System","path":"/system","hidden":false,"redirect":"noRedirect","component":"Layout","alwaysShow":true,"meta":{"title":"系统管理","icon":"system","noCache":false},"children":[{"name":"User","path":"user","hidden":false,"component":"permission/user/index","meta":{"title":"用户管理","icon":"user","noCache":false}},{"name":"Role","path":"role","hidden":false,"component":"permission/role/index","meta":{"title":"角色管理","icon":"peoples","noCache":false}},{"name":"Menu","path":"menu","hidden":false,"component":"permission/menu/index","meta":{"title":"菜单管理","icon":"tree-table","noCache":false}},{"name":"Dept","path":"dept","hidden":false,"component":"permission/dept/index","meta":{"title":"部门管理","icon":"tree","noCache":false}},{"name":"Post","path":"post","hidden":false,"component":"permission/post/index","meta":{"title":"岗位管理","icon":"post","noCache":false}},{"name":"Dict","path":"dict","hidden":false,"component":"system/dict/index","meta":{"title":"字典管理","icon":"dict","noCache":false}},{"name":"Config","path":"config","hidden":false,"component":"system/config/index","meta":{"title":"参数设置","icon":"edit","noCache":false}},{"name":"Notice","path":"notice","hidden":false,"component":"system/notice/index","meta":{"title":"通知公告","icon":"message","noCache":false}},{"name":"Log","path":"log","hidden":false,"redirect":"noRedirect","component":"ParentView","alwaysShow":true,"meta":{"title":"日志管理","icon":"log","noCache":false},"children":[{"name":"Operlog","path":"operlog","hidden":false,"component":"monitor/operlog/index","meta":{"title":"操作日志","icon":"form","noCache":false}},{"name":"Logininfor","path":"logininfor","hidden":false,"component":"monitor/logininfor/index","meta":{"title":"登录日志","icon":"logininfor","noCache":false}}]}]},{"name":"Monitor","path":"/monitor","hidden":false,"redirect":"noRedirect","component":"Layout","alwaysShow":true,"meta":{"title":"系统监控","icon":"monitor","noCache":false},"children":[{"name":"Online","path":"online","hidden":false,"component":"monitor/online/index","meta":{"title":"在线用户","icon":"online","noCache":false}},{"name":"Job","path":"job","hidden":false,"component":"monitor/job/index","meta":{"title":"定时任务","icon":"job","noCache":false}},{"name":"Druid","path":"druid","hidden":false,"component":"monitor/druid/index","meta":{"title":"数据监控","icon":"druid","noCache":false}},{"name":"Server","path":"server","hidden":false,"component":"monitor/server/index","meta":{"title":"服务监控","icon":"server","noCache":false}},{"name":"Cache","path":"cache","hidden":false,"component":"monitor/cache/index","meta":{"title":"缓存监控","icon":"redis","noCache":false}}]},{"name":"Tool","path":"/tool","hidden":false,"redirect":"noRedirect","component":"Layout","alwaysShow":true,"meta":{"title":"系统工具","icon":"tool","noCache":false},"children":[{"name":"Build","path":"build","hidden":false,"component":"tool/build/index","meta":{"title":"表单构建","icon":"build","noCache":false}},{"name":"Gen","path":"gen","hidden":false,"component":"tool/gen/index","meta":{"title":"代码生成","icon":"code","noCache":false}},{"name":"Swagger","path":"swagger","hidden":false,"component":"tool/swagger/index","meta":{"title":"系统接口","icon":"swagger","noCache":false}}]},{"name":"Http://ruoyi.vip","path":"http://ruoyi.vip","hidden":false,"component":"Layout","meta":{"title":"若依官网","icon":"guide","noCache":false}}]}'
        data = json.loads(data)
        return Response(data)


class MenuModelViewSet(CustomModelViewSet):
    """
    菜单模型 的CRUD视图
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    create_serializer_class = MenuCreateUpdateSerializer
    update_serializer_class = MenuCreateUpdateSerializer
    filter_class = MenuFilter
    # update_extra_permission_classes = (IsManagerPermission,)
    # destroy_extra_permission_classes = (IsManagerPermission,)
    # create_extra_permission_classes = (IsManagerPermission,)
    search_fields = ('name',)
    ordering = 'create_datetime'  # 默认排序


class DeptModelViewSet(CustomModelViewSet):
    """
    部门管理 的CRUD视图
    """
    queryset = Dept.objects.all()
    serializer_class = DeptSerializer
    create_serializer_class = DeptCreateUpdateSerializer
    update_serializer_class = DeptCreateUpdateSerializer
    filter_class = DeptFilter
    # update_extra_permission_classes = (IsManagerPermission,)
    # destroy_extra_permission_classes = (IsManagerPermission,)
    # create_extra_permission_classes = (IsManagerPermission,)
    search_fields = ('name',)
    ordering = 'create_datetime'  # 默认排序

    def exclude_list(self, request: Request, *args, **kwargs):
        dept_queryset = Dept.objects.filter(id=kwargs.get('pk')).first()
        parentId = dept_queryset.parentId if dept_queryset else ''
        queryset = self.queryset.exclude(parentId=parentId).order_by('orderNum')
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, *args, **kwargs)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(serializer.data)


class PostModelViewSet(CustomModelViewSet):
    """
    岗位管理 的CRUD视图
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    create_serializer_class = PostCreateUpdateSerializer
    update_serializer_class = PostCreateUpdateSerializer
    filter_class = PostFilter
    # update_extra_permission_classes = (IsManagerPermission,)
    # destroy_extra_permission_classes = (IsManagerPermission,)
    # create_extra_permission_classes = (IsManagerPermission,)
    search_fields = ('name',)
    ordering = ['postSort','create_datetime']  # 默认排序


class RoleModelViewSet(CustomModelViewSet):
    """
    角色管理 的CRUD视图
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    create_serializer_class = RoleCreateUpdateSerializer
    update_serializer_class = RoleCreateUpdateSerializer
    filter_class = RoleFilter
    # update_extra_permission_classes = (IsManagerPermission,)
    # destroy_extra_permission_classes = (IsManagerPermission,)
    # create_extra_permission_classes = (IsManagerPermission,)
    search_fields = ('name',)
    ordering = 'create_datetime'  # 默认排序

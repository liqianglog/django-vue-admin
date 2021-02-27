from django.contrib.auth import authenticate
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.op_drf.viewsets import CustomModelViewSet
from apps.permission.filters import MenuFilter, DeptFilter, PostFilter, RoleFilter, UserProfileFilter
from apps.permission.models import Role, Menu, Dept, Post, UserProfile
from apps.permission.serializers import UserProfileSerializer, MenuSerializer, RoleSerializer, \
    MenuCreateUpdateSerializer, DeptSerializer, DeptCreateUpdateSerializer, PostSerializer, PostCreateUpdateSerializer, \
    RoleCreateUpdateSerializer, DeptTreeSerializer, MenuTreeSerializer, UserProfileCreateUpdateSerializer, \
    PostSimpleSerializer, RoleSimpleSerializer
from utils.response import SuccessResponse, ErrorResponse


class GetUserProfileView(APIView):
    """
    获取用户详细信息
    """

    def get(self, request, format=None):
        user_dict = UserProfileSerializer(request.user).data
        permissions_list = ["*:*:*"] if user_dict.get('admin') else Menu.objects.filter(
            role__userprofile=request.user).values_list('perms', flat=True)
        return SuccessResponse({
            'permissions': [ele for ele in permissions_list if ele],
            'roles': Role.objects.filter(userprofile=request.user).values_list('roleKey', flat=True),
            'user': user_dict
        })


class GetRouters(APIView):
    """
    获取路由详细信息
    """

    def depth_menu(self, menus):
        """
        获取菜单(通过前端递归值)
        :param menus:
        :return:
        """

        return dict

    def get(self, request, format=None):
        # data = GetUserInfoSerializer(request.user).data
        menus = Menu.objects.filter(role__userprofile=request.user).exclude(menuType="2").values('id','name', 'web_path',
                                                                                                 'visible', 'status',
                                                                                                 'isFrame',
                                                                                                 'component_path',
                                                                                                 'icon', 'parentId',
                                                                                                 'isCache')
        # data = '{"msg":"操作成功","code":200,"data":[{"name":"System","path":"/system","hidden":false,"redirect":"noRedirect","component":"Layout","alwaysShow":true,"meta":{"title":"系统管理","icon":"system","noCache":false},"children":[{"name":"User","path":"user","hidden":false,"component":"permission/user/index","meta":{"title":"用户管理","icon":"user","noCache":false}},{"name":"Role","path":"role","hidden":false,"component":"permission/role/index","meta":{"title":"角色管理","icon":"peoples","noCache":false}},{"name":"Menu","path":"menu","hidden":false,"component":"permission/menu/index","meta":{"title":"菜单管理","icon":"tree-table","noCache":false}},{"name":"Dept","path":"dept","hidden":false,"component":"permission/dept/index","meta":{"title":"部门管理","icon":"tree","noCache":false}},{"name":"Post","path":"post","hidden":false,"component":"permission/post/index","meta":{"title":"岗位管理","icon":"post","noCache":false}},{"name":"Dict","path":"dict","hidden":false,"component":"system/dict/index","meta":{"title":"字典管理","icon":"dict","noCache":false}},{"name":"Config","path":"config","hidden":false,"component":"system/config/index","meta":{"title":"参数设置","icon":"edit","noCache":false}},{"name":"Notice","path":"notice","hidden":false,"component":"system/notice/index","meta":{"title":"通知公告","icon":"message","noCache":false}},{"name":"Log","path":"log","hidden":false,"redirect":"noRedirect","component":"ParentView","alwaysShow":true,"meta":{"title":"日志管理","icon":"log","noCache":false},"children":[{"name":"Operlog","path":"operlog","hidden":false,"component":"monitor/operlog/index","meta":{"title":"操作日志","icon":"form","noCache":false}},{"name":"Logininfor","path":"logininfor","hidden":false,"component":"monitor/logininfor/index","meta":{"title":"登录日志","icon":"logininfor","noCache":false}}]}]},{"name":"Monitor","path":"/monitor","hidden":false,"redirect":"noRedirect","component":"Layout","alwaysShow":true,"meta":{"title":"系统监控","icon":"monitor","noCache":false},"children":[{"name":"Online","path":"online","hidden":false,"component":"monitor/online/index","meta":{"title":"在线用户","icon":"online","noCache":false}},{"name":"Job","path":"job","hidden":false,"component":"monitor/job/index","meta":{"title":"定时任务","icon":"job","noCache":false}},{"name":"Druid","path":"druid","hidden":false,"component":"monitor/druid/index","meta":{"title":"数据监控","icon":"druid","noCache":false}},{"name":"Server","path":"server","hidden":false,"component":"monitor/server/index","meta":{"title":"服务监控","icon":"server","noCache":false}},{"name":"Cache","path":"cache","hidden":false,"component":"monitor/cache/index","meta":{"title":"缓存监控","icon":"redis","noCache":false}}]},{"name":"Tool","path":"/tool","hidden":false,"redirect":"noRedirect","component":"Layout","alwaysShow":true,"meta":{"title":"系统工具","icon":"tool","noCache":false},"children":[{"name":"Build","path":"build","hidden":false,"component":"tool/build/index","meta":{"title":"表单构建","icon":"build","noCache":false}},{"name":"Gen","path":"gen","hidden":false,"component":"tool/gen/index","meta":{"title":"代码生成","icon":"code","noCache":false}},{"name":"Swagger","path":"swagger","hidden":false,"component":"tool/swagger/index","meta":{"title":"系统接口","icon":"swagger","noCache":false}}]},{"name":"Http://ruoyi.vip","path":"http://ruoyi.vip","hidden":false,"component":"Layout","meta":{"title":"若依官网","icon":"guide","noCache":false}}]}'
        # data = json.loads(data)
        data = []
        for ele in menus:
            data.append({
                'id': ele.get('id'),
                'name': ''.join([i.capitalize() for i in ele.get('web_path','').split('/')]),
                'path': ele.get('web_path'),
                'hidden': True if ele.get('visible') != '1' else False,
                'redirect': ele.get('web_path') if ele.get('isFrame') == '1' else 'noRedirect',
                'component': ele.get('component_path') or 'Layout',
                'meta': {"title": ele.get('name'), "icon": ele.get('icon'), "noCache": ele.get('isCache')},
                'parentId': ele.get('parentId')
            })
        return SuccessResponse(data)


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

    def tree_select_list(self, request: Request, *args, **kwargs):
        """
        递归获取部门树
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        queryset = self.filter_queryset(self.get_queryset())
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, *args, **kwargs)
        serializer = MenuTreeSerializer(queryset, many=True)
        return SuccessResponse(serializer.data)

    def role_menu_tree_select(self, request: Request, *args, **kwargs):
        """
        根据角色ID查询菜单下拉树结构
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        menu_queryset = Menu.objects.filter(role__id=kwargs.get('pk')).values_list('id', flat=True)
        queryset = self.filter_queryset(self.get_queryset())
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, *args, **kwargs)
        serializer = MenuTreeSerializer(queryset, many=True)
        return SuccessResponse({
            'menus': serializer.data,
            'checkedKeys': menu_queryset
        })


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
    search_fields = ('deptName',)
    ordering = 'create_datetime'  # 默认排序

    def exclude_list(self, request: Request, *args, **kwargs):
        """
        过滤剔除同级部门
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        dept_queryset = Dept.objects.filter(id=kwargs.get('pk')).first()
        parentId = dept_queryset.parentId if dept_queryset else ''
        queryset = self.queryset.exclude(parentId=parentId).order_by('orderNum')
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, *args, **kwargs)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(serializer.data)

    def tree_select_list(self, request: Request, *args, **kwargs):
        """
        递归获取部门树
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        queryset = self.filter_queryset(self.get_queryset())
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, *args, **kwargs)
        serializer = DeptTreeSerializer(queryset, many=True)
        return SuccessResponse(serializer.data)

    def role_dept_tree_select(self, request: Request, *args, **kwargs):
        """
        根据角色ID查询部门树结构
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        dept_queryset = Dept.objects.filter(role__id=kwargs.get('pk')).values_list('id', flat=True)
        queryset = self.filter_queryset(self.get_queryset())
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, *args, **kwargs)
        serializer = DeptTreeSerializer(queryset, many=True)
        return SuccessResponse({
            'depts': serializer.data,
            'checkedKeys': dept_queryset
        })


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
    search_fields = ('postName',)
    ordering = ['postSort', 'create_datetime']  # 默认排序


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
    search_fields = ('roleName',)
    ordering = 'create_datetime'  # 默认排序


class UserProfileModelViewSet(CustomModelViewSet):
    """
    用户管理 的CRUD视图
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    create_serializer_class = UserProfileCreateUpdateSerializer
    update_serializer_class = UserProfileCreateUpdateSerializer
    filter_class = UserProfileFilter
    # update_extra_permission_classes = (IsManagerPermission,)
    # destroy_extra_permission_classes = (IsManagerPermission,)
    # create_extra_permission_classes = (IsManagerPermission,)
    search_fields = ('username',)
    ordering = 'create_datetime'  # 默认排序

    def change_status(self, request: Request, *args, **kwargs):
        """
        修改用户状态
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.queryset.get(id=request.data.get('userId'))
        instance.is_active = request.data.get('status')
        instance.save()
        serializer = self.get_serializer(instance)
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, instance=instance, *args, **kwargs)
        return SuccessResponse(serializer.data)

    def get_user_details(self, request: Request, *args, **kwargs):
        """
        获取用户详情
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        userId = request.query_params.get('userId')
        data = {
            'posts': PostSimpleSerializer(Post.objects.all().order_by('postSort'), many=True).data,
            'roles': RoleSimpleSerializer(Role.objects.all().order_by('roleSort'), many=True).data
        }
        if userId:
            instance = self.queryset.get(id=userId)
            serializer = self.get_serializer(instance)
            data['data'] = serializer.data
            data['postIds'] = [ele.get('id') for ele in serializer.data.get('post')]
            data['roleIds'] = [ele.get('id') for ele in serializer.data.get('role')]
            if hasattr(self, 'handle_logging'):
                self.handle_logging(request, instance=instance, *args, **kwargs)
        return SuccessResponse(data)

    def reset_pwd(self, request: Request, *args, **kwargs):
        """
        重置密码
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.queryset.get(id=request.data.get('userId'))
        serializer = self.get_serializer(instance)
        instance.set_password(request.data.get('password'))
        instance.save()
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, instance=instance, *args, **kwargs)
        return SuccessResponse(serializer.data)

    def profile(self, request: Request, *args, **kwargs):
        """
        获取用户个人信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.queryset.get(id=request.user.id)
        serializer = self.get_serializer(instance)
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, instance=instance, *args, **kwargs)
        return SuccessResponse(serializer.data)

    def put_profile(self, request: Request, *args, **kwargs):
        """
        更新用户个人信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.queryset.get(id=request.user.id)
        instance.name = request.data.get('name',None)
        instance.mobile = request.data.get('mobile',None)
        instance.email = request.data.get('email',None)
        instance.gender = request.data.get('gender',None)
        instance.save()
        serializer = self.get_serializer(instance)
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, instance=instance, *args, **kwargs)
        return SuccessResponse(serializer.data)


    def update_pwd(self, request: Request, *args, **kwargs):
        """
        个人修改密码
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.queryset.get(id=request.user.id)
        instance.mobile = request.data.get('newPassword',None)
        if not authenticate(username=request.user.username, password=request.data.get('oldPassword',None)):
            return ErrorResponse(msg='旧密码不正确！')
        instance.set_password(request.data.get('newPassword'))
        instance.save()
        serializer = self.get_serializer(instance)
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, instance=instance, *args, **kwargs)
        return SuccessResponse(serializer.data)

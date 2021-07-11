from django.urls import re_path
from rest_framework.routers import DefaultRouter

from apps.vadmin.permission.views import MenuModelViewSet, DeptModelViewSet, PostModelViewSet, RoleModelViewSet, \
    UserProfileModelViewSet

router = DefaultRouter()
router.register(r'menus', MenuModelViewSet)
router.register(r'dept', DeptModelViewSet)
router.register(r'dept/exclude', DeptModelViewSet)
router.register(r'post', PostModelViewSet)
router.register(r'role', RoleModelViewSet)
router.register(r'user', UserProfileModelViewSet)
urlpatterns = [

    re_path('dept/exclude/(?P<pk>.*)/', DeptModelViewSet.as_view({'get': 'exclude_list'})),
    re_path('dept/treeselect/', DeptModelViewSet.as_view({'get': 'tree_select_list'})),
    re_path('menus/treeselect/', MenuModelViewSet.as_view({'get': 'tree_select_list'})),
    # 根据角色ID查询菜单下拉树结构
    re_path('menus/roleMenuTreeselect/(?P<pk>.*)/', MenuModelViewSet.as_view({'get': 'role_menu_tree_select'})),
    # 根据角色ID查询部门树结构
    re_path('dept/roleDeptTreeselect/(?P<pk>.*)/', DeptModelViewSet.as_view({'get': 'role_dept_tree_select'})),
    # 更新状态
    re_path('user/changeStatus/', UserProfileModelViewSet.as_view({'put': 'change_status'})),
    # 获取用户详情
    re_path('user/details/', UserProfileModelViewSet.as_view({'get': 'get_user_details'})),
    # 后台重置密码
    re_path('user/resetPwd/', UserProfileModelViewSet.as_view({'put': 'reset_pwd'})),
    # 用户自己重置密码
    re_path('user/profile/updatePwd/', UserProfileModelViewSet.as_view({'put': 'update_pwd'})),
    # 更新用户头像
    re_path('user/profile/avatar/', UserProfileModelViewSet.as_view({'put': 'put_avatar'})),
    # 获取、更新用户个人信息
    re_path('user/profile/', UserProfileModelViewSet.as_view({'get': 'profile', 'put': 'put_profile'})),
    # 导出用户
    re_path('user/export/', UserProfileModelViewSet.as_view({'get': 'export', })),
    # 导出角色
    re_path('role/export/', RoleModelViewSet.as_view({'get': 'export', })),
    # 导出岗位
    re_path('post/export/', PostModelViewSet.as_view({'get': 'export', })),
    # 用户导入模板下载及导入
    re_path('user/importTemplate/',
            UserProfileModelViewSet.as_view({'get': 'importTemplate', 'post': 'importTemplate'})),

]
urlpatterns += router.urls

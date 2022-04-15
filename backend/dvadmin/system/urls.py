# -*- coding: utf-8 -*-

"""
@author: 猿小天
@contact: QQ:1638245306
@Created on: 2021/6/1 001 23:05
@Remark: 系统管理的路由文件
"""
from django.urls import path
from rest_framework import routers

from dvadmin.system.views.api_white_list import ApiWhiteListViewSet
from dvadmin.system.views.area import AreaViewSet
from dvadmin.system.views.button import ButtonViewSet
from dvadmin.system.views.dept import DeptViewSet
from dvadmin.system.views.dictionary import DictionaryViewSet
from dvadmin.system.views.file_list import FileViewSet
from dvadmin.system.views.menu import MenuViewSet
from dvadmin.system.views.menu_button import MenuButtonViewSet
from dvadmin.system.views.operation_log import OperationLogViewSet
from dvadmin.system.views.role import RoleViewSet
from dvadmin.system.views.system_config import SystemConfigViewSet
from dvadmin.system.views.user import UserViewSet

system_url = routers.SimpleRouter()
system_url.register(r'menu', MenuViewSet)
system_url.register(r'button', ButtonViewSet)
system_url.register(r'menu_button', MenuButtonViewSet)
system_url.register(r'role', RoleViewSet)
system_url.register(r'dept', DeptViewSet)
system_url.register(r'user', UserViewSet)
system_url.register(r'operation_log', OperationLogViewSet)
system_url.register(r'dictionary', DictionaryViewSet)
system_url.register(r'area', AreaViewSet)
system_url.register(r'file', FileViewSet)
system_url.register(r'api_white_list', ApiWhiteListViewSet)
system_url.register(r'system_config', SystemConfigViewSet)

urlpatterns = [
    path('role/roleId_get_menu/<int:pk>/', RoleViewSet.as_view({'get': 'roleId_get_menu'})),
    path('menu/web_router/', MenuViewSet.as_view({'get': 'web_router'})),
    path('user/user_info/', UserViewSet.as_view({'get': 'user_info', 'put': 'update_user_info'})),
    path('user/change_password/<int:pk>/', UserViewSet.as_view({'put': 'change_password'})),
    path('user/reset_password/<int:pk>/', UserViewSet.as_view({'put': 'reset_password'})),
    path('user/export/', UserViewSet.as_view({'post': 'export_data', })),
    path('user/import/',UserViewSet.as_view({'get': 'import_data', 'post': 'import_data'})),
    path('system_config/save_content/', SystemConfigViewSet.as_view({'put': 'save_content'})),
    path('system_config/get_association_table/', SystemConfigViewSet.as_view({'get': 'get_association_table'})),
    path('system_config/get_table_data/<int:pk>/', SystemConfigViewSet.as_view({'get': 'get_table_data'})),
    path('system_config/get_relation_info/', SystemConfigViewSet.as_view({'get': 'get_relation_info'})),
]
urlpatterns += system_url.urls

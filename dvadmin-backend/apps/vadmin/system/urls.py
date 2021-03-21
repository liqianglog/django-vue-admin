from django.urls import re_path
from rest_framework.routers import DefaultRouter

from ..system.views import DictDataModelViewSet, DictDetailsModelViewSet, \
    ConfigSettingsModelViewSet, SaveFileModelViewSet, MessagePushModelViewSet, LoginInforModelViewSet, \
    OperationLogModelViewSet

router = DefaultRouter()
router.register(r'dict/type', DictDataModelViewSet)
router.register(r'dict/data', DictDetailsModelViewSet)
router.register(r'config', ConfigSettingsModelViewSet)
router.register(r'savefile', SaveFileModelViewSet)
router.register(r'message', MessagePushModelViewSet)
router.register(r'logininfor', LoginInforModelViewSet)
router.register(r'operation_log', OperationLogModelViewSet)

urlpatterns = [
    re_path('dict/get/type/(?P<pk>.*)/', DictDetailsModelViewSet.as_view({'get': 'dict_details_list'})),
    re_path('config/configKey/(?P<pk>.*)/', ConfigSettingsModelViewSet.as_view({'get': 'get_config_key'})),
    # 参数管理导出
    re_path('config/export/', ConfigSettingsModelViewSet.as_view({'get': 'export'})),
    # 导出字典管理数据
    re_path('dict/type/export/', DictDataModelViewSet.as_view({'get': 'export'})),
    # 导出字典详情数据
    re_path('dict/data/export/', DictDetailsModelViewSet.as_view({'get': 'export'})),
    # 用户获取个人消息通知列表页
    re_path('message/list/(?P<pk>.*)/', MessagePushModelViewSet.as_view({"get": "get_message_list"})),
    # 用户获取个人通知列表
    re_path('message/receive/', MessagePushModelViewSet.as_view({"get": "get_received_messages"})),
    # 消息通知导出
    re_path('message/export/', MessagePushModelViewSet.as_view({'get': 'export', })),
    # 用户个人消息列表
    re_path('message/user_messages/', MessagePushModelViewSet.as_view({'get': 'get_user_messages', })),
    # 改为已读
    re_path('message/is_read/(?P<pk>.*)/', MessagePushModelViewSet.as_view({'put': 'update_is_read', })),
    # 清空操作日志
    re_path('operation_log/clean/', OperationLogModelViewSet.as_view({'delete': 'clean_all', })),
    # 导出操作日志
    re_path('operation_log/export/', OperationLogModelViewSet.as_view({'get': 'export', })),
]
urlpatterns += router.urls

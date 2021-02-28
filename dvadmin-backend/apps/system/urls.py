from django.urls import re_path
from rest_framework.routers import DefaultRouter

from apps.system.views import DictDataModelViewSet, DictDetailsModelViewSet, \
    ConfigSettingsModelViewSet, SaveFileModelViewSet

router = DefaultRouter()
router.register(r'dict/type', DictDataModelViewSet)
router.register(r'dict/data', DictDetailsModelViewSet)
router.register(r'config', ConfigSettingsModelViewSet)
router.register(r'savefile', SaveFileModelViewSet)
urlpatterns = [
    re_path('dict/get/type/(?P<pk>.*)/', DictDetailsModelViewSet.as_view({'get': 'dict_details_list'})),
    re_path('config/configKey/(?P<pk>.*)/', ConfigSettingsModelViewSet.as_view({'get': 'get_config_key'})),
    # 参数管理导出
    re_path('config/export/', ConfigSettingsModelViewSet.as_view({'get': 'export'})),
    # 导出字典管理数据
    re_path('dict/type/export/', DictDataModelViewSet.as_view({'get': 'export'})),
    # 导出字典详情数据
    re_path('dict/data/export/', DictDetailsModelViewSet.as_view({'get': 'export'})),
]
urlpatterns += router.urls

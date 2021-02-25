from django.urls import re_path
from rest_framework.routers import DefaultRouter

from apps.system.views import DictDataModelViewSet, DictDetailsModelViewSet, DictDetailsListModelViewSet

router = DefaultRouter()
router.register(r'dict/type', DictDataModelViewSet)
router.register(r'dict/data', DictDetailsModelViewSet)
router.register(r'dict/get/type', DictDetailsListModelViewSet)
urlpatterns = [
]
urlpatterns += router.urls

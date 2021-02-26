from django.urls import re_path
from rest_framework.routers import DefaultRouter

from apps.system.views import DictDataModelViewSet, DictDetailsModelViewSet, DictDetailsListModelViewSet

router = DefaultRouter()
router.register(r'dict/type', DictDataModelViewSet)
router.register(r'dict/data', DictDetailsModelViewSet)
urlpatterns = [
    re_path('dict/get/type/(?P<pk>.*)/', DictDetailsListModelViewSet.as_view({'get':'list'})),
]
urlpatterns += router.urls

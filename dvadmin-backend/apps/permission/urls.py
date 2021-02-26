from django.urls import re_path
from rest_framework.routers import DefaultRouter

from apps.permission.views import MenuModelViewSet, DeptModelViewSet, PostModelViewSet, RoleModelViewSet

router = DefaultRouter()
router.register(r'menus', MenuModelViewSet)
router.register(r'dept', DeptModelViewSet)
router.register(r'dept/exclude', DeptModelViewSet)
router.register(r'post', PostModelViewSet)
router.register(r'role', RoleModelViewSet)
urlpatterns = [

    re_path('dept/exclude/(?P<pk>.*)/', DeptModelViewSet.as_view({'get': 'exclude_list'}), name='api_token_auth'),

]
urlpatterns += router.urls

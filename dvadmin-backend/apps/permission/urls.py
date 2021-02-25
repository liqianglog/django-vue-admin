from django.urls import re_path
from rest_framework.routers import DefaultRouter

from apps.permission.views import MenuModelViewSet

router = DefaultRouter()
router.register(r'menus', MenuModelViewSet)
urlpatterns = [

    # re_path('menus/', MenuModelViewSet.as_view({'get': 'list'}), name='api_token_auth'),

]
urlpatterns += router.urls

from django.urls import path
from rest_framework import routers

from kfm_apps.carton_manage.ipc_api.views.code_package import CodePackageViewSet
from kfm_apps.carton_manage.ipc_api.views.code_package_template import CodePackageTemplateViewSet

url = routers.SimpleRouter()

urlpatterns = [
    path('code_package/',CodePackageViewSet.as_view({'get':'list'})),
    path('code_package_template/',CodePackageTemplateViewSet.as_view({'get':'list'}))
]
urlpatterns += url.urls


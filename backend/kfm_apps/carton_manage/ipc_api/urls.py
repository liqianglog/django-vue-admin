from django.urls import path
from rest_framework import routers

from carton_manage.ipc_api.views.production_work import ProductionWorkViewSet
from carton_manage.ipc_api.views.code_package import CodePackageViewSet
from carton_manage.ipc_api.views.code_package_template import CodePackageTemplateViewSet

url = routers.SimpleRouter()
url.register(r'code_package_template', CodePackageTemplateViewSet)
url.register(r'production_work', ProductionWorkViewSet)

urlpatterns = [
    path('code_package/', CodePackageViewSet.as_view({'post': 'list'})),
    path(r'download_code_package_file/<str:tenant_name>/<str:day>/<str:file_name>',
         CodePackageViewSet.as_view({'post': 'download_code_package_file'}))

]
urlpatterns += url.urls

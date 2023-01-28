from rest_framework import routers

from basics_manage.views.code_package_template import CodePackageTemplateViewSet
from basics_manage.views.device_manage import DeviceManageViewSet
from basics_manage.views.factory_info import FactoryInfoViewSet
from basics_manage.views.production_line import ProductionLineViewSet

url = routers.SimpleRouter()
url.register(r'factory_info', FactoryInfoViewSet)
url.register(r'device_manage', DeviceManageViewSet)
url.register(r'production_line', ProductionLineViewSet)
url.register(r'code_package_template', CodePackageTemplateViewSet)

urlpatterns = [
]
urlpatterns += url.urls

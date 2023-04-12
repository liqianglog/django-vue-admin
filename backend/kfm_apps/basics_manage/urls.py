from rest_framework import routers

from basics_manage.views.code_package_format import CodePackageFormatViewSet
from basics_manage.views.code_package_template import CodePackageTemplateViewSet
from basics_manage.views.customer_info import CustomerInfoViewSet
from basics_manage.views.device_manage import DeviceManageViewSet
from basics_manage.views.factory_info import FactoryInfoViewSet
from basics_manage.views.production_line import ProductionLineViewSet

url = routers.SimpleRouter()
url.register(r'factory_info', FactoryInfoViewSet)
url.register(r'device_manage', DeviceManageViewSet)
url.register(r'production_line', ProductionLineViewSet)
url.register(r'code_package_template', CodePackageTemplateViewSet)
url.register(r'code_package_format', CodePackageFormatViewSet)
url.register(r'customer_info', CustomerInfoViewSet)
urlpatterns = [
]
urlpatterns += url.urls

from rest_framework import routers

from carton_manage.code_manage.views.code_package import CodePackageViewSet

url = routers.SimpleRouter()
url.register(r'code_package', CodePackageViewSet)
urlpatterns = [
]
urlpatterns += url.urls

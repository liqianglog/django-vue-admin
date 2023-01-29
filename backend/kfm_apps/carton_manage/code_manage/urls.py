from django.urls import re_path
from rest_framework import routers

from application import settings
from carton_manage.code_manage.views.code_package import CodePackageViewSet

url = routers.SimpleRouter()
url.register(r'code_package', CodePackageViewSet)
urlpatterns = [
    #re_path(r'^code_package/download_file/(.*)$', CodePackageViewSet.download_file, {'document_root': settings.MEDIA_ROOT})
]
urlpatterns += url.urls

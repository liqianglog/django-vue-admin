from django.urls import re_path
from rest_framework import routers

from application import settings
from carton_manage.code_manage.views.code_package import CodePackageViewSet
from carton_manage.code_manage.views.code_repetition_record import CodeRepetitionRecordViewSet

url = routers.SimpleRouter()
url.register(r'code_package', CodePackageViewSet)
url.register(r'code_repetition_record', CodeRepetitionRecordViewSet)

urlpatterns = [

]
urlpatterns += url.urls

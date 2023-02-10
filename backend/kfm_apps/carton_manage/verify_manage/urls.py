from rest_framework import routers

from carton_manage.verify_manage.views.back_haul_file import BackHaulFileViewSet
from carton_manage.verify_manage.views.camera_manage import CameraManageViewSet
from carton_manage.verify_manage.views.verify_code_record import VerifyCodeRecordViewSet
from carton_manage.verify_manage.views.verify_work_order import VerifyWorkOrderViewSet

url = routers.SimpleRouter()
url.register(r'camera_manage', CameraManageViewSet)
url.register(r'back_haul_file', BackHaulFileViewSet)
url.register(r'verify_code_record', VerifyCodeRecordViewSet)
url.register(r'verify_work_order', VerifyWorkOrderViewSet)


urlpatterns = [
]
urlpatterns += url.urls

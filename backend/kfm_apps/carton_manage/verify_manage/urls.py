from rest_framework import routers

from carton_manage.verify_manage.views.camera_manage import CameraManageViewSet

url = routers.SimpleRouter()
url.register(r'camera_manage', CameraManageViewSet)



urlpatterns = [
]
urlpatterns += url.urls

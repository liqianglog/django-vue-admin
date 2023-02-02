from rest_framework import routers

from carton_manage.production_manage.views.production_work import ProductionWorkViewSet
from carton_manage.production_manage.views.production_work_status_record import ProductionWorkStatusRecordViewSet
from carton_manage.production_manage.views.production_work_verify_record import ProductionWorkVerifyRecordViewSet

url = routers.SimpleRouter()
url.register(r'production_work', ProductionWorkViewSet)
url.register(r'production_work_status_record', ProductionWorkStatusRecordViewSet)
url.register(r'production_work_verify_record', ProductionWorkVerifyRecordViewSet)


urlpatterns = [
]
urlpatterns += url.urls

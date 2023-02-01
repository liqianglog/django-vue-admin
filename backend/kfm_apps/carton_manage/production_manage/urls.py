from rest_framework import routers

from carton_manage.production_manage.views.production_work import ProductionWorkViewSet

url = routers.SimpleRouter()
url.register(r'production_work', ProductionWorkViewSet)
urlpatterns = [
]
urlpatterns += url.urls

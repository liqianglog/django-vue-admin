from rest_framework.routers import DefaultRouter

from .views import ServerModelViewSet, MonitorModelViewSet

router = DefaultRouter()
router.register(r'server', ServerModelViewSet)
router.register(r'monitor', MonitorModelViewSet)

urlpatterns = [

]
urlpatterns += router.urls

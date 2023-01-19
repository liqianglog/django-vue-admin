from rest_framework import routers

from dvadmin_tenants.views.tenant_client import ClientViewSet
from dvadmin_tenants.views.tenant_domain import DomainViewSet

url = routers.SimpleRouter()
url.register(r'client', ClientViewSet)
url.register(r'domain', DomainViewSet)

urlpatterns = [
]
urlpatterns += url.urls

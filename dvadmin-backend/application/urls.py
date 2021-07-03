"""application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from captcha.conf import settings as ca_settings
from captcha.helpers import captcha_image_url, captcha_audio_url
from captcha.models import CaptchaStore
from django.conf import settings
from django.urls import re_path, include
from django.views.static import serve
from rest_framework.views import APIView

from apps.vadmin.op_drf.response import SuccessResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

class CaptchaRefresh(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        new_key = CaptchaStore.pick()
        to_json_response = {
            "key": new_key,
            "image_url": captcha_image_url(new_key),
            "audio_url": captcha_audio_url(new_key) if ca_settings.CAPTCHA_FLITE_PATH else None,
        }
        return SuccessResponse(to_json_response)


urlpatterns = [
    re_path(r'media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r'^admin/', include('apps.vadmin.urls')),
    re_path(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

from django.urls import path, include, re_path


urlpatterns = [
    re_path('basics_manage/', include('carton_manage.basics_manage.urls')),
]

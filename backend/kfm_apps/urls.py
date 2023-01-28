from django.urls import path, include, re_path


urlpatterns = [
    re_path('basics_manage/', include('basics_manage.urls')),  # 基础模块
    # # 纸箱
    re_path('carton/code_manage/', include('carton_manage.code_manage.urls')),  # 码包管理
    re_path('carton/production_manage/', include('carton_manage.production_manage.urls')),  # 生产管理
    re_path('basics_manage/', include('carton_manage.basics_manage.urls')), # 基础模块
    re_path('carton/ipc/', include('carton_manage.ipc_api.urls')), # 工控机接口
]

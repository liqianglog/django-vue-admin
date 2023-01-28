from django.urls import include, re_path

from basics_manage.views.device_manage import DeviceManageLogin

urlpatterns = [
    re_path('device_login/', DeviceManageLogin.as_view()),  # 设备登录
    re_path('basics_manage/', include('basics_manage.urls')),  # 基础模块
    # # 纸箱
    re_path('carton/code_manage/', include('carton_manage.code_manage.urls')),  # 码包管理
    re_path('carton/production_manage/', include('carton_manage.production_manage.urls')),  # 生产管理
    re_path('carton/ipc/', include('carton_manage.ipc_api.urls')),  # 工控机接口
]

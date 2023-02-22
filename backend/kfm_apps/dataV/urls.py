# -*- coding: utf-8 -*-
from django.urls import path

from dataV.number_info import *

urlpatterns = [
    path('number_info/',NumberInfoApiView.as_view()),
    path('code_package_repetition_pie/',CodePackageRepetitionPieAPIView.as_view()),
    path('device_info/',DeviceInfoAPIView.as_view()),
    path('production_work/',ProductionWorkAPIView.as_view()),
    path('verify_code_record/',VerifyCodeRecordAPIView.as_view()),
    path('verify_code_pie/',VerifyCodePieAPIView.as_view()),
]


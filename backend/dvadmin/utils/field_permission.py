# -*- coding: utf-8 -*-
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from dvadmin.system.models import Columns
from dvadmin.utils.json_response import DetailResponse
from dvadmin.utils.models import get_custom_app_models


class FieldPermissionMixin:
    @action(methods=['get'], detail=False,permission_classes=[IsAuthenticated])
    def field_permission(self, request):
        """
        获取字段权限
        """
        finded = False
        for app in get_custom_app_models():
            for model in app:
                if model['object'] is self.serializer_class.Meta.model:
                    finded = True
                    break
            if finded:
                break
        if finded is False:
            return []
        data= Columns.objects.filter(
            app=model['app'], model=model['model']
        ).values('field_name', 'is_create', 'is_query', 'is_update')
        return DetailResponse(data=data)
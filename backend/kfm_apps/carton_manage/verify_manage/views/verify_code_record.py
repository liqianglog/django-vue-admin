import django_filters
from django_filters.rest_framework import FilterSet
from rest_framework import serializers

from carton_manage.verify_manage.models import VerifyCodeRecord
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class VerifyCodeRecordSerializer(CustomModelSerializer):
    """
   校验码记录-序列化器
    """
    class Meta:
        model = VerifyCodeRecord
        fields = "__all__"
        read_only_fields = ["id"]


class VerifyCodeRecordCreateUpdateSerializer(CustomModelSerializer):
    """
   校验码记录管理 创建/更新时的列化器
    """

    class Meta:
        model = VerifyCodeRecord
        fields = '__all__'


class VerifyCodeRecordFilterSet(FilterSet):
    # factory_info_name = django_filters.CharFilter(field_name="factory_info__name", lookup_expr="icontains")
    # production_line_name = django_filters.CharFilter(field_name="production_line__name", lookup_expr="icontains")
    # device_name = django_filters.CharFilter(field_name="device__name", lookup_expr="icontains")

    class Meta:
        model = VerifyCodeRecord
        fields = '__all__'

class VerifyCodeRecordViewSet(CustomModelViewSet):
    """
   校验码记录管理接口:
    """
    queryset = VerifyCodeRecord.objects.all()
    serializer_class = VerifyCodeRecordSerializer
    create_serializer_class = VerifyCodeRecordCreateUpdateSerializer
    update_serializer_class = VerifyCodeRecordCreateUpdateSerializer

    def get_queryset(self):
        params = self.request.query_params
        if params:
            exclude_success = params.get('exclude_success',False)
            if exclude_success:
                return VerifyCodeRecord.objects.filter(error_type__in=[0,2,3,4,5]).all()
        return VerifyCodeRecord.objects.all()

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
    camera_no = serializers.CharField(source='back_haul_file.cam.no',read_only=True,default="")
    factory_info_name = serializers.CharField(source="back_haul_file.device.production_line.factory_info.name", read_only=True,default="")
    production_line_name = serializers.CharField(source="back_haul_file.device.production_line.name", read_only=True,default="")
    device_name = serializers.CharField(source="back_haul_file.device.name", read_only=True,default="")

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

class VerifyCodeRecordExportSerializer(CustomModelSerializer):
    """
   校验码记录导出-序列化器
    """
    camera_no = serializers.CharField(source='back_haul_file.cam.no',read_only=True,default="")
    factory_info_name = serializers.CharField(source="back_haul_file.device.production_line.factory_info.name", read_only=True,default="")
    production_line_name = serializers.CharField(source="back_haul_file.device.production_line.name", read_only=True,default="")
    device_name = serializers.CharField(source="back_haul_file.device.name", read_only=True,default="")
    code_type_label = serializers.CharField(source='get_code_type_display',read_only=True)
    error_type_label = serializers.CharField(source='get_error_type_display', read_only=True)
    class Meta:
        model = VerifyCodeRecord
        fields = "__all__"
        read_only_fields = ["id"]

class VerifyCodeRecordFilterSet(FilterSet):
    camera_no = django_filters.CharFilter(field_name='back_haul_file__cam__no', lookup_expr="icontains")
    factory_info_name = django_filters.CharFilter(field_name="back_haul_file__device__production_line__factory_info__name", lookup_expr="icontains")
    production_line_name = django_filters.CharFilter(field_name="back_haul_file__device__production_line__name", lookup_expr="icontains")
    device_name = django_filters.CharFilter(field_name="back_haul_file__device__name", lookup_expr="icontains")

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
    export_serializer_class = VerifyCodeRecordExportSerializer
    filter_class = VerifyCodeRecordFilterSet
    export_field_label = {
        "code_content_md5": "码内容",
        "code_type_label": "码类型",
        "ac_time": "采集时间",
        "error_type_label": "问题码类型",
        "camera_no": "相机编号",
        "factory_info_name": "生产工厂",
        "production_line_name": "生产产线",
        "device_name": "生产设备",
    }

    def get_queryset(self):
        params = self.request.query_params
        if params:
            exclude_success = params.get('exclude_success',False)
            if exclude_success:
                return VerifyCodeRecord.objects.filter(error_type__in=[0,2,3,4,5]).all()
        return VerifyCodeRecord.objects.all()

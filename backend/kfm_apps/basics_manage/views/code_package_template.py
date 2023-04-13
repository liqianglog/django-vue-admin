import django_filters
from rest_framework import serializers

from basics_manage.models import CodePackageTemplate, CodePackageTemplateAttribute
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet

class AttributeFiledSerializer(CustomModelSerializer):

    class Meta:
        model = CodePackageTemplateAttribute
        fields = '__all__'
        extra_kwargs = {'code_package_template': {'required': False,'allow_null':True}}

class CodePackageTemplateSerializer(CustomModelSerializer):
    """
    码包模板-序列化器
    """
    customer_name = serializers.CharField(source="customer.name",read_only=True)
    attr_fields = serializers.SerializerMethodField()

    def get_attr_fields(self, instance):
        fields = AttributeFiledSerializer(instance.codepackagetemplateattribute_set.all(),many=True)
        return fields.data
    class Meta:
            model = CodePackageTemplate
            fields = "__all__"
            read_only_fields = ["id"]


class CodePackageTemplateCreateUpdateSerializer(CustomModelSerializer):
    """
    码包模板管理 创建/更新时的列化器
    """
    class Meta:
        model = CodePackageTemplate
        fields = '__all__'
    def create(self, validated_data):
        instance = CodePackageTemplate.objects.create(**validated_data)
        init_data = self.initial_data
        attr_fields = init_data.get("attr_fields",[])
        serializer = AttributeFiledSerializer(data=attr_fields,many=True,request=self.request)
        serializer.is_valid(raise_exception=True)
        serializer.save(code_package_template=instance)
        return instance

    def update(self, instance, validated_data):
        init_data = self.initial_data
        attr_fields = init_data.get("attr_fields", [])
        need_update_id = []
        for item in attr_fields:
            id = item.get("id", None)
            need_update_id.append(id)
            queryset = CodePackageTemplateAttribute.objects.filter(id=id).first()
            if queryset:
                serializer = AttributeFiledSerializer(instance=queryset,data=item, many=False, request=self.request)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            else:
                serializer = AttributeFiledSerializer(data=item, many=False, request=self.request)
                serializer.is_valid(raise_exception=True)
                serializer.save(code_package_template=instance)
        CodePackageTemplateAttribute.objects.exclude(id__in=need_update_id).delete()
        return super().update(instance, validated_data)

class CodePackageTemplateFilter(django_filters.FilterSet):
    id = django_filters.AllValuesMultipleFilter(field_name="id",lookup_expr='in')
    class Meta:
        model = CodePackageTemplate
        fields = "__all__"

class CodePackageTemplateViewSet(CustomModelViewSet):
    """
    码包模板管理接口:
    """
    queryset = CodePackageTemplate.objects.all()
    serializer_class = CodePackageTemplateSerializer
    create_serializer_class = CodePackageTemplateCreateUpdateSerializer
    update_serializer_class = CodePackageTemplateCreateUpdateSerializer
    search_fields = ['no', 'name']

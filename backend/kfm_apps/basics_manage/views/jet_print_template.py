from rest_framework import serializers

from basics_manage.models import JetPrintTemplate, JetPrintTemplateAttribute
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet

class JPTAttributeFiledSerializer(CustomModelSerializer):

    class Meta:
        model = JetPrintTemplateAttribute
        fields = '__all__'
        extra_kwargs = {'code_package_template': {'required': False,'allow_null':True}}

class JetPrintTemplateSerializer(CustomModelSerializer):
    """
    喷码模板-序列化器
    """
    customer_name = serializers.CharField(source="customer.name",read_only=True)
    attr_fields = serializers.SerializerMethodField()

    def get_attr_fields(self, instance):
        fields = JPTAttributeFiledSerializer(instance.JetPrintTemplateattribute_set.all(),many=True)
        return fields.data
    class Meta:
            model = JetPrintTemplate
            fields = "__all__"
            read_only_fields = ["id"]


class JetPrintTemplateCreateUpdateSerializer(CustomModelSerializer):
    """
    喷码模板管理 创建/更新时的列化器
    """
    class Meta:
        model = JetPrintTemplate
        fields = '__all__'
    def create(self, validated_data):
        code_package_template = validated_data.pop('code_package_template')
        instance = JetPrintTemplate.objects.create(**validated_data)
        instance.code_package_template.set(code_package_template)
        init_data = self.initial_data
        attr_fields = init_data.get("attr_fields",[])
        serializer = JPTAttributeFiledSerializer(data=attr_fields,many=True,request=self.request)
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
            queryset = JetPrintTemplateAttribute.objects.filter(id=id).first()
            if queryset:
                serializer = JPTAttributeFiledSerializer(instance=queryset,data=item, many=False, request=self.request)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            else:
                serializer = JPTAttributeFiledSerializer(data=item, many=False, request=self.request)
                serializer.is_valid(raise_exception=True)
                serializer.save(code_package_template=instance)
        JetPrintTemplateAttribute.objects.exclude(id__in=need_update_id).delete()
        return super().update(instance, validated_data)

class JetPrintTemplateViewSet(CustomModelViewSet):
    """
    喷码模板管理接口:
    """
    queryset = JetPrintTemplate.objects.all()
    serializer_class = JetPrintTemplateSerializer
    create_serializer_class = JetPrintTemplateCreateUpdateSerializer
    update_serializer_class = JetPrintTemplateCreateUpdateSerializer
    search_fields = ['no', 'name']

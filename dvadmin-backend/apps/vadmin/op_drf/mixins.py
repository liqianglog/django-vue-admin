from rest_framework import mixins
from rest_framework import serializers
from rest_framework import status
from rest_framework.relations import ManyRelatedField, RelatedField, PrimaryKeyRelatedField
from rest_framework.request import Request

from .response import SuccessResponse


class CreateModelMixin(mixins.CreateModelMixin):
    """
    继承、增强DRF的CreateModelMixin, 标准化其返回值
    """
    create_serializer_class = None

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, instance=serializer.instance, *args, **kwargs)
        headers = self.get_success_headers(serializer.data)
        return SuccessResponse(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        super().perform_create(serializer)


class ListModelMixin(mixins.ListModelMixin):
    """
    继承、增强DRF的CreateModelMixin, 标准化其返回值
    """
    list_serializer_class = None

    def list(self, request: Request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, *args, **kwargs)
        if page is not None:
            if getattr(self, 'values_queryset', None):
                return self.get_paginated_response(page)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        if getattr(self, 'values_queryset', None):
            return SuccessResponse(page)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(serializer.data)


class RetrieveModelMixin(mixins.RetrieveModelMixin):
    """
    继承、增强DRF的CreateModelMixin, 标准化其返回值
    """
    retrieve_serializer_class = None

    def retrieve(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, instance=instance, *args, **kwargs)
        return SuccessResponse(serializer.data)


class UpdateModelMixin(mixins.UpdateModelMixin):
    """
    继承、增强DRF的CreateModelMixin, 标准化其返回值
    """
    update_serializer_class = None

    def update(self, request: Request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, instance=instance, *args, **kwargs)
        return SuccessResponse(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class DestroyModelMixin(mixins.DestroyModelMixin):
    """
    继承、增强DRF的CreateModelMixin, 标准化其返回值
    """
    destroy_serializer_class = None

    def destroy(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, instance=instance, *args, **kwargs)
        return SuccessResponse(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class TableSerializerMixin:
    table_option = None
    extra_columns = []

    FIELD_TYPE_MAP = {
        'AutoField': {
            'type': 'input',
            'addDisabled': True,
        },

        'CharField': {
            'type': 'input',
            "maxlength": 255
        },

        'PasswordField': {
            'type': 'input',
            'maxlength': 255
        },

        'URLField': {
            'type': 'input',
        },

        'UUIDField': {
            'type': 'input',
            'minlength': 32,
            'maxlength': 32,
        },

        'UUID8Field': {
            'type': 'input',
            'minlength': 8,
            'maxlength': 8,
        },

        'UUID16Field': {
            'type': 'input',
            'minlength': 16,
            'maxlength': 16,
        },

        'UUID32Field': {
            'type': 'input',
            'minlength': 32,
            'maxlength': 32,
        },

        'UUID36Field': {
            'type': 'input',
            'minlength': 36,
            'maxlength': 36
        },

        'DateTimeField': {
            'type': 'datetime',
            'format': "yyyy-MM-dd hh:mm:ss",
            'valueFormat': "yyyy-MM-dd hh:mm:ss",
        },
        'DateField': {
            'type': 'date',
            'format': "yyyy-MM-dd",
            'valueFormat': "yyyy-MM-dd",
        },

        'TimeField': {
            'type': 'time',
            'format': "hh:mm:ss",
            'valueFormat': "hh:mm:ss",
        },

        'BooleanField': {
            'type': 'radio',
            'dicData': [
                {'value': False, 'label': '否'},
                {'value': True, 'label': '是'},
            ]
        },

        'ManyRelatedField': {
            # 'type': 'select',
            'type': 'array',
            # "multiple": True,
            'required': False,
        },
    }

    FIELD_TYPE_DEFAULT = {
        'type': 'input',
    }

    def getTable(self, serializer: serializers.ModelSerializer = None):
        if not serializer:
            serializer = self.get_serializer()
        serializer_class = serializer.__class__
        model = serializer_class.Meta.model
        title = model.__name__
        if hasattr(model, 'Meta'):
            if hasattr(model.Meta, 'verbose_name'):
                title = model.Meta.verbose_name or ''
        column = self.getColumn(serializer)
        table = {
            'title': title,
            'page': True,
            'align': 'center',
            'menuAlign': 'center',
            'columnBtn': True,
            'menu': True,
            'menuType': 'icon',
            'addBtn': True,
            'delBtn': True,
            'editBtn': True,
            'column': column
        }
        return table

    def getColumn(self, serializer: serializers.ModelSerializer = None):
        if not serializer:
            serializer = self.get_serializer()
        serializer_class = serializer.__class__
        fields = serializer.get_fields()
        show_fields = getattr(serializer_class.Meta, 'show_fields', set())
        hide_fields = getattr(serializer_class.Meta, 'hide_fields', set())
        search_fields = getattr(serializer_class.Meta, 'search_fields', set())
        sortable_fields = getattr(serializer_class.Meta, 'sortable_fields', set())
        column = []
        for prop in fields:
            field = fields[prop]
            field_type = field.__class__.__name__
            info = {
                'prop': prop,
                'label': field.label or prop,
                'hide': hide_fields == '__all__' or prop in hide_fields,
                'search': search_fields == '__all__' or prop in search_fields,
                'sortable': sortable_fields == '__all__' or prop in sortable_fields,
                'width': 'auto',
                'align': 'left',
                'overHidden': False,
            }
            type_info = self.FIELD_TYPE_MAP.get(field_type, self.FIELD_TYPE_DEFAULT)
            info.update(type_info)

            allow_null = getattr(field, 'allow_null', False)
            allow_blank = getattr(field, 'allow_blank', False)
            allow_empty = getattr(field, 'allow_empty', False)

            read_only = getattr(field, 'read_only', False)
            write_only = getattr(field, 'write_only', False)

            if not any([allow_null, allow_blank, allow_empty]):
                rules = [{
                    'required': True,
                    'message': f"""请输入{info['label']}""",
                    'trigger': "blur"
                }]
                info['rules'] = rules
            if read_only:
                info['editDisabled'] = True,
                info['clearable'] = False

            if not isinstance(field, (ManyRelatedField, RelatedField, PrimaryKeyRelatedField)):
                # 防止序列化该字段的关系模型所有数据
                choices = getattr(field, 'choices', None)
                if choices:
                    dicData = list(map(lambda choice: {'value': choice[0], 'label': choice[1]}, choices.items()))
                    info['dicData'] = dicData
                    info['type'] = 'select'
            column.append(info)
        return column

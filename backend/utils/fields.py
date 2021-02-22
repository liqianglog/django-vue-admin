from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import SET_NULL

from .string_util import uuid_8, uuid_16, uuid_32, uuid_36


class IdField(models.CharField):
    """
    id = IdField()
    """

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 8)
        kwargs['primary_key'] = kwargs.get('primary_key', True)
        kwargs['unique'] = kwargs.get('unique', True)
        kwargs['db_index'] = kwargs.get('db_index', True)
        kwargs['default'] = kwargs.get('default', uuid_8)
        kwargs['null'] = kwargs.get('null', False)
        kwargs['blank'] = kwargs.get('blank', False)
        kwargs['verbose_name'] = kwargs.get('verbose_name', 'ID')
        kwargs['help_text'] = kwargs.get('help_text', 'ID')
        super().__init__(*args, **kwargs)


class UUID8Field(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 8)
        kwargs['default'] = kwargs.get('default', uuid_8)
        kwargs['verbose_name'] = kwargs.get('verbose_name', 'UUID')
        kwargs['help_text'] = kwargs.get('help_text', 'UUID')
        super().__init__(*args, **kwargs)


class UUID16Field(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 16)
        kwargs['default'] = kwargs.get('default', uuid_16)
        kwargs['verbose_name'] = kwargs.get('verbose_name', 'UUID')
        kwargs['help_text'] = kwargs.get('help_text', 'UUID')
        super().__init__(*args, **kwargs)


class UUID32Field(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 32)
        kwargs['default'] = kwargs.get('default', uuid_32)
        kwargs['verbose_name'] = kwargs.get('verbose_name', 'UUID')
        kwargs['help_text'] = kwargs.get('help_text', 'UUID')
        super().__init__(*args, **kwargs)


class UUID36Field(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 36)
        kwargs['unique'] = kwargs.get('unique', True)
        kwargs['default'] = kwargs.get('default', uuid_36)
        kwargs['verbose_name'] = kwargs.get('verbose_name', 'UUID')
        kwargs['help_text'] = kwargs.get('help_text', 'UUID')
        super().__init__(*args, **kwargs)


class DescriptionField(models.TextField):
    """
    description = DescriptionField()
    """

    def __init__(self, *args, **kwargs):
        kwargs['default'] = kwargs.get('default', '')
        kwargs['blank'] = kwargs.get('blank', True)
        kwargs['null'] = kwargs.get('null', True)
        kwargs['verbose_name'] = kwargs.get('verbose_name', '描述')
        kwargs['help_text'] = kwargs.get('help_text', '') or kwargs.get('verbose_name', '描述')
        super().__init__(*args, **kwargs)


class TextField(models.TextField):
    """
    xxx = TextField()
    """

    def __init__(self, *args, **kwargs):
        kwargs['default'] = kwargs.get('default', '')
        kwargs['blank'] = kwargs.get('blank', True)
        kwargs['null'] = kwargs.get('null', True)
        kwargs['verbose_name'] = kwargs.get('verbose_name', '')
        kwargs['help_text'] = kwargs.get('help_text', '') or kwargs.get('verbose_name', '')
        super().__init__(*args, **kwargs)


class CharField(models.CharField):
    """
    xxx = CharField()
    """

    def __init__(self, *args, **kwargs):
        kwargs['default'] = kwargs.get('default', '')
        kwargs['blank'] = kwargs.get('blank', True)
        kwargs['null'] = kwargs.get('null', True)
        kwargs['verbose_name'] = kwargs.get('verbose_name', '')
        kwargs['help_text'] = kwargs.get('help_text', '') or kwargs.get('verbose_name', '')
        super().__init__(*args, **kwargs)


class IntegerField(models.IntegerField):
    """
    xxx = IntegerField()
    """

    def __init__(self, *args, **kwargs):
        kwargs['default'] = kwargs.get('default', 0)
        kwargs['verbose_name'] = kwargs.get('verbose_name', '')
        kwargs['help_text'] = kwargs.get('help_text', '') or kwargs.get('verbose_name', '')
        super().__init__(*args, **kwargs)


class BooleanField(models.BooleanField):
    """
    xxx = BooleanField()
    """

    def __init__(self, *args, **kwargs):
        kwargs['verbose_name'] = kwargs.get('verbose_name', '')
        kwargs['help_text'] = kwargs.get('help_text', '') or kwargs.get('verbose_name', '')
        super().__init__(*args, **kwargs)


class DateField(models.DateField):
    """
    xxx = DateField()
    """

    def __init__(self, *args, **kwargs):
        kwargs['verbose_name'] = kwargs.get('verbose_name', '')
        kwargs['help_text'] = kwargs.get('help_text', '') or kwargs.get('verbose_name', '')
        kwargs['editable'] = kwargs.get('default', False)
        kwargs['blank'] = kwargs.get('blank', True)
        kwargs['null'] = kwargs.get('null', True)
        super().__init__(*args, **kwargs)


class DateTimeField(models.DateTimeField):
    """
    xxx = DateTimeField()
    """

    def __init__(self, *args, **kwargs):
        kwargs['verbose_name'] = kwargs.get('verbose_name', '')
        kwargs['help_text'] = kwargs.get('help_text', '') or kwargs.get('verbose_name', '')
        kwargs['editable'] = kwargs.get('default', False)
        kwargs['blank'] = kwargs.get('blank', True)
        kwargs['null'] = kwargs.get('null', True)
        super().__init__(*args, **kwargs)


class ForeignKey(models.ForeignKey):
    """
    xxx = ForeignKey()
    """

    def __init__(self, to=None, on_delete=None, related_name=None, related_query_name=None, limit_choices_to=None,
                 parent_link=False, to_field=None, db_constraint=False, **kwargs):
        if on_delete is None:
            on_delete = SET_NULL
        if to_field is None:
            to_field = 'id'
        kwargs['verbose_name'] = kwargs.get('verbose_name', '')
        kwargs['help_text'] = kwargs.get('help_text', '') or kwargs.get('verbose_name', '')
        kwargs['editable'] = kwargs.get('default', False)
        kwargs['blank'] = kwargs.get('blank', True)
        kwargs['null'] = kwargs.get('null', True)
        super().__init__(to, on_delete, related_name, related_query_name, limit_choices_to, parent_link, to_field,
                         db_constraint, **kwargs)


class OneToOneField(models.OneToOneField):
    """
    xxx = OneToOneField()
    """

    def __init__(self, *args, on_delete=None, to_field=None, db_constraint=False, **kwargs):
        if on_delete is None:
            on_delete = SET_NULL
        if to_field is None:
            to_field = 'id'
        kwargs['verbose_name'] = kwargs.get('verbose_name', '')
        kwargs['help_text'] = kwargs.get('help_text', '') or kwargs.get('verbose_name', '')
        kwargs['editable'] = kwargs.get('default', None)
        kwargs['blank'] = kwargs.get('blank', True)
        kwargs['null'] = kwargs.get('null', True)
        super().__init__(*args, on_delete=on_delete, to_field=to_field, db_constraint=db_constraint, **kwargs)


class ManyToManyField(models.ManyToManyField):
    """
    xxx = ManyToManyField()
    """

    def __init__(self, *args, db_constraint=False, **kwargs):
        kwargs['verbose_name'] = kwargs.get('verbose_name', '')
        kwargs['help_text'] = kwargs.get('help_text', '') or kwargs.get('verbose_name', '')
        kwargs['editable'] = kwargs.get('default', False)
        kwargs['blank'] = kwargs.get('blank', True)
        super().__init__(*args, db_constraint=db_constraint, **kwargs)


class UserForeignKeyField(models.ForeignKey):
    """
    user = UserForeignKeyField()
    """

    def __init__(self, to=None, on_delete=None, related_name=None, related_query_name=None, limit_choices_to=None,
                 parent_link=False, to_field=None, db_constraint=False, **kwargs):
        if to is None:
            to = get_user_model()
        if to_field is None:
            to_field = 'id'
        if on_delete is None:
            on_delete = SET_NULL
        kwargs['verbose_name'] = kwargs.get('verbose_name', '关联的用户')
        kwargs['help_text'] = kwargs.get('help_text', '') or kwargs.get('verbose_name', '关联的用户')
        kwargs['editable'] = kwargs.get('default', False)
        kwargs['blank'] = kwargs.get('blank', True)
        kwargs['null'] = kwargs.get('null', True)
        super().__init__(to, on_delete, related_name, related_query_name, limit_choices_to, parent_link, to_field,
                         db_constraint, **kwargs)


class UpdateDateTimeField(models.DateTimeField):
    """
    update_datetime = ModifyDateTimeField()
    """

    def __init__(self, verbose_name=None, name=None, auto_now=True, auto_now_add=False, **kwargs):
        verbose_name = verbose_name or '修改时间'
        kwargs['help_text'] = kwargs.get('help_text', '修改时间')
        kwargs['editable'] = kwargs.get('default', False)
        kwargs['blank'] = kwargs.get('blank', True)
        kwargs['null'] = kwargs.get('null', True)
        super().__init__(verbose_name, name, auto_now, auto_now_add, **kwargs)


class CreateDateTimeField(models.DateTimeField):
    """
    create_datetime = CreateDateTimeField()
    """

    def __init__(self, verbose_name=None, name=None, auto_now=False, auto_now_add=True, **kwargs):
        verbose_name = verbose_name or '创建时间'
        kwargs['help_text'] = kwargs.get('help_text', '创建时间')
        kwargs['editable'] = kwargs.get('default', False)
        kwargs['blank'] = kwargs.get('blank', True)
        kwargs['null'] = kwargs.get('null', True)
        super().__init__(verbose_name, name, auto_now, auto_now_add, **kwargs)


class CreatorCharField(CharField):
    """
    creator = CreatorCharField()
    """

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 255)
        kwargs['null'] = kwargs.get('null', True)
        kwargs['blank'] = kwargs.get('blank', True)
        kwargs['verbose_name'] = kwargs.get('verbose_name', '创建者')
        kwargs['help_text'] = kwargs.get('help_text', '该记录的创建者')
        super().__init__(*args, **kwargs)


class ModifierCharField(CharField):
    """
    modifier = ModifierCharField()
    """

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 255)
        kwargs['null'] = kwargs.get('null', True)
        kwargs['blank'] = kwargs.get('blank', True)
        kwargs['verbose_name'] = kwargs.get('verbose_name', '修改者')
        kwargs['help_text'] = kwargs.get('help_text', '该记录最后修改者')
        super().__init__(*args, **kwargs)

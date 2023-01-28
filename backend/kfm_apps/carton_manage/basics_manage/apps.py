from django.apps import AppConfig


class BasicsManageConfig(AppConfig):
    """
    基础信息
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'carton_manage.basics_manage'

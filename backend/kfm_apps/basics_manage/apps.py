from django.apps import AppConfig


class BasicsManageConfig(AppConfig):
    """
    基础信息
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'basics_manage'

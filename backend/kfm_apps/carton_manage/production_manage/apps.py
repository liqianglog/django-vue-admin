from django.apps import AppConfig


class ProductionManageConfig(AppConfig):
    """
    生产管理
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'carton_manage.production_manage'

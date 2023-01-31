from django.apps import AppConfig


class DvadminCeleryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dvadmin_celery'
    url_prefix = "dvadmin_celery"

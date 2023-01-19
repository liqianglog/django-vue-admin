from django.apps import AppConfig


class DvadminTenantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dvadmin_tenants'
    url_prefix = "tenant"

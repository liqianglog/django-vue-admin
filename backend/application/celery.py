import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')

from django.conf import settings
from celery import platforms

if getattr(settings, 'REGISTER_PLUGINS', {}).get('dvadmin_tenant', None):
    from tenant_schemas_celery.app import CeleryApp as TenantAwareCeleryApp
    app = TenantAwareCeleryApp()
else:
    from celery import Celery

    app = Celery(f"application")
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
platforms.C_FORCE_ROOT = True

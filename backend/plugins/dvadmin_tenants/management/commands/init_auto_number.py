import logging

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.core.management.color import no_style
from django.db import connection
from django_tenants.utils import get_tenant_model, tenant_context

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    重置所有库表自增id: python manage.py init_auto_number
    """

    def handle(self, *args, **options):
        for tenant in get_tenant_model().objects.all():
            with tenant_context(tenant):
                for content_type in ContentType.objects.all():
                    model = content_type.model_class()
                    if not model:
                        continue
                    sequence_sql = connection.ops.sequence_reset_sql(no_style(), [model])
                    with connection.cursor() as cursor:
                        for sql in sequence_sql:
                            try:
                                cursor.execute(sql)
                            except Exception as e:
                                pass
        print(f"重置所有库表自增id完成")

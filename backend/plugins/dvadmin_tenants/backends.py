import datetime
import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db import connection
from django.utils import timezone
from rest_framework.exceptions import APIException

from dvadmin_tenants.models import Client

logger = logging.getLogger(__name__)
UserModel = get_user_model()


class TenantCustomBackend(ModelBackend):
    """
    租户认证方式，校验租户是否过期和是否启用
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        msg = '正在校验租户是否过期或是否启用...'
        logger.info(msg)
        client = Client.objects.filter(schema_name=connection.tenant.schema_name).first()
        now_date = datetime.date.today()
        if client.start_datetime > now_date:
            raise APIException(detail=f"该企业尚未生效，生效日期：{client.start_datetime}，请联系管理员！")
        if client.paid_until < now_date:
            raise APIException(detail=f"该企业已过期，过期日期：{client.paid_until}，请联系管理员！")

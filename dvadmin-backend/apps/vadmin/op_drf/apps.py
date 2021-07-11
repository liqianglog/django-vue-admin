import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class OpDrfConfig(AppConfig):
    name = 'apps.vadmin.op_drf'
    verbose_name = "OP DRF"

    def ready(self):
        logging.info("OP DRF框架检测完成:success")

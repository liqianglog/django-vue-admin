import logging
import os

from django.core.management.base import BaseCommand
from django.db import connection

from scripts import getSql

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    项目初始化命令: python manage.py initialization
    """

    def customSql(self, sql_list):
        """
        批量执行sql
        :param sql_list:
        :return:
        """
        with connection.cursor() as cursor:
            for sql in sql_list:
                cursor.execute(sql)
            connection.commit()

    def init(self, sql_filename, model_name):
        """
        初始化
        :param sql_filename: sql存放位置
        :param model_name: 模块名
        :return:
        """
        logger.info(f'正在初始化[{model_name}]中...')
        self.customSql(getSql(sql_filename))
        logger.info(f'[{model_name}]初始化完成！')


    def handle(self, *args, **options):
        self.init(os.path.join('system', 'system_dictdata.sql'), '字典管理')
        self.init(os.path.join('system', 'system_dictdetails.sql'), '字典详情')
        self.init(os.path.join('system', 'system_configsettings.sql'), '参数设置')
        self.init(os.path.join('permission', 'permission_post.sql'), '岗位管理')
        self.init(os.path.join('permission', 'permission_dept.sql'), '部门管理')
        self.init(os.path.join('permission', 'permission_menu.sql'), '菜单管理')
        self.init(os.path.join('permission', 'permission_role.sql'), '角色管理')
        self.init(os.path.join('permission', 'permission_userprofile.sql'), '用户管理')

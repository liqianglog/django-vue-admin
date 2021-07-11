import logging
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection

from apps.vadmin.scripts import getSql

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    项目初始化命令: python manage.py init
    """

    def customSql(self, sql_list, model_name, table_name, is_yes):
        """
        批量执行sql
        :param sql_list:
        :param table_name: 表名
        :return:
        """
        with connection.cursor() as cursor:
            num = 0
            for ele in table_name.split(','):
                cursor.execute("select count(*) from {}".format(ele))
                result = cursor.fetchone()
                num += result[0]
            if num > 0:
                while True:
                    if is_yes is None:
                        inp = input(f'[{model_name}]模型已初始化完成，继续将清空[{table_name}]表中所有数据，是否继续初始化？【 Y/N 】')
                    else:
                        inp = 'Y' if is_yes == True else 'N'
                    if inp.upper() == 'N':
                        return False
                    elif inp.upper() == 'Y':
                        logger.info(f'正在清空[{table_name}]中数据...')
                        cursor.execute("SET foreign_key_checks = 0")
                        for ele in table_name.split(','):
                            cursor.execute("truncate table {};".format(ele))
                        cursor.execute("SET foreign_key_checks = 1")
                        connection.commit()
                        logger.info(f'清空[{table_name}]中数据{result[0]}条')
                        break

            for sql in sql_list:
                try:
                    cursor.execute(sql)
                except Exception as e:
                    print(e)
            connection.commit()
            return True

    def init(self, sql_filename, model_name, table_name, is_yes):
        """
        初始化
        :param sql_filename: sql存放位置
        :param model_name: 模块名
        :param table_name: 表名
        :return:
        """
        logger.info(f'正在初始化[{model_name}]中...')
        if self.customSql(getSql(sql_filename), model_name, table_name, is_yes):
            logger.info(f'[{model_name}]初始化完成！')
        else:
            logger.info(f'已取消[{table_name}]初始化')

    def add_arguments(self, parser):
        parser.add_argument('init_name', nargs='*', type=str, )
        parser.add_argument('-y', nargs='*')
        parser.add_argument('-Y', nargs='*')
        parser.add_argument('-n', nargs='*')
        parser.add_argument('-N', nargs='*')

    def handle(self, *args, **options):
        user_name = "_".join(settings.AUTH_USER_MODEL.lower().split("."))
        init_dict = {
            'system_dictdata': [os.path.join('system', 'system_dictdata.sql'), '字典管理', 'system_dictdata'],
            'system_dictdetails': [os.path.join('system', 'system_dictdetails.sql'), '字典详情', 'system_dictdetails'],
            'system_configsettings': [os.path.join('system', 'system_configsettings.sql'), '参数设置',
                                      'system_configsettings'],
            'permission_post': [os.path.join('permission', 'permission_post.sql'), '岗位管理', 'permission_post'],
            'permission_dept': [os.path.join('permission', 'permission_dept.sql'), '部门管理', 'permission_dept'],
            'permission_menu': [os.path.join('permission', 'permission_menu.sql'), '菜单管理', 'permission_menu'],
            'permission_role': [os.path.join('permission', 'permission_role.sql'), '角色管理',
                                ','.join(['permission_role', 'permission_role_dept', 'permission_role_menu'])],
            'permission_userprofile': [os.path.join('permission', 'permission_userprofile.sql'), '用户管理', ','.join(
                [f'{user_name}_groups', f'{user_name}', f'{user_name}_role', f'{user_name}_post'])]
        }
        init_name = options.get('init_name')
        is_yes = None
        if isinstance(options.get('y'), list) or isinstance(options.get('Y'), list):
            is_yes = True
        if isinstance(options.get('n'), list) or isinstance(options.get('N'), list):
            is_yes = False
        if init_name:
            [self.init(*init_dict[ele], is_yes=is_yes) for ele in init_name if ele in init_dict]
        else:
            for ele in init_dict.values():
                self.init(*ele, is_yes=is_yes)

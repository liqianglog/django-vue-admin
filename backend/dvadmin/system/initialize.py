# 初始化
import os

import django

from dvadmin.utils.core_initialize import CoreInitialize

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "application.settings")
django.setup()

from dvadmin.system.models import (
    Dept,
    Button,
    Menu,
    MenuButton,
    Role,
    Users,
)

from .init_data import (
    dept_data,
    button_data,
    menu_data,
    menu_button_data,
    role_data,
    staff_data,
    dictionary_data,
)


class Initialize(CoreInitialize):
    creator_id = 1

    def init_dept(self):
        """
        初始化部门信息
        """
        self.dept_data = dept_data
        self.save(Dept, self.dept_data, "部门信息")

    def init_button(self):
        """
        初始化按钮表
        """
        self.button_data = button_data
        self.save(Button, self.button_data, "权限表标识")

    def init_menu(self):
        """
        初始化菜单表
        """
        self.menu_data = menu_data
        self.save(Menu, self.menu_data, "菜单表")

    def init_menu_button(self):
        """
        初始化菜单按钮表
        """
        self.menu_button_data = menu_button_data
        self.save(MenuButton, self.menu_button_data, "菜单权限表")

    def init_role(self):
        """
        初始化角色表
        """
        data = role_data
        self.save(Role, data, "角色表")

    def init_users(self):
        """
        初始化用户表
        """
        data = staff_data
        self.save(Users, data, "用户表", no_reset=False)

    def init_dictionary(self):
        """
        初始化字典表
        """
        data = dictionary_data
        self.save(Users, data, "字典表", no_reset=False)

    def run(self):
        self.init_dept()
        self.init_button()
        self.init_menu()
        self.init_menu_button()
        self.init_role()
        self.init_users()


# 项目init 初始化，默认会执行 main 方法进行初始化
def main(reset=False):
    Initialize(reset).run()


if __name__ == "__main__":
    main()

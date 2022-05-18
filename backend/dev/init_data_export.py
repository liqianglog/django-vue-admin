# 初始化
import json
from _venv import *
from django.core import serializers


from dvadmin.system.models import (
    Dept,
    Button,
    Menu,
    MenuButton,
    Role,
    Users,
    Dictionary,
)


def export_data():
    db_dept_data = (
        Dept.objects.all().values("id", "name", "sort", "parent").order_by("id")
    )
    for dept in db_dept_data:
        dept["parent_id"] = dept.pop("parent")
    db_button_data = Button.objects.all().values("id", "name", "value").order_by("id")
    db_menu_data = (
        Menu.objects.all()
        .values(
            "id",
            "name",
            "sort",
            "web_path",
            "icon",
            "is_catalog",
            "visible",
            "parent",
            "component",
            "component_name",
        )
        .order_by("id")
    )
    for menu in db_menu_data:
        menu["parent_id"] = menu.pop("parent")
    db_menu_button_data = (
        MenuButton.objects.all()
        .values("id", "menu", "name", "value", "api", "method")
        .order_by("id")
    )
    for menu in db_menu_button_data:
        menu["menu_id"] = menu.pop("menu")
    db_dictionary_data = (
        Dictionary.objects.all()
        .values("id", "label", "value", "status", "sort")
        .order_by("id")
    )
    db_staff_data = (
        Users.objects.all()
        .values(
            "id",
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "username",
            "name",
            "email",
            "mobile",
            "dept",
        )
        .order_by("id")
    )
    db_role_data = (
        Role.objects.all()
        .values("id", "name", "key", "sort", "status", "admin", "data_range")
        .order_by("id")
    )

    data_dict = {
        "dept_data": db_dept_data,
        "button_data": db_button_data,
        "menu_data": db_menu_data,
        "menu_button_data": db_menu_button_data,
        "dictionary_data": db_dictionary_data,
    }

    with open("../dvadmin/system/util/init_data.py", "w", encoding="utf8") as f:
        for k, item in data_dict.items():
            f.write(f"{k} = [\n")
            for obj in item:
                f.write("\t")
                f.write(str(obj))
                f.write(",\n")
            f.write("]\n\n")

        f.write(f"role_data = [\n")
        json_data = json.loads(serializers.serialize("json", Role.objects.all()))
        for index, obj in enumerate(db_role_data):
            obj["dept"] = json_data[index]["fields"]["dept"]
            obj["menu"] = json_data[index]["fields"]["menu"]
            obj["permission"] = json_data[index]["fields"]["permission"]
            f.write("\t")
            f.write(str(obj))
            f.write(",\n")
        f.write("]\n\n")

        f.write(f"staff_data = [\n")
        json_data = json.loads(serializers.serialize("json", Users.objects.all()))
        for index, obj in enumerate(db_staff_data):
            obj["dept_id"] = obj.pop("dept")
            obj["role"] = json_data[index]["fields"]["role"]
            f.write("\t")
            f.write(str(obj))
            f.write(",\n")
        f.write("]\n\n")


if __name__ == "__main__":
    # 生成初始化data
    export_data()  # 调试用, 可先禁用settings.INSTALLED_APPS中的自定义app

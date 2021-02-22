from django.db.models import SET_DEFAULT

from utils import fields
from utils.BaseModels import CoreModel


class Menu(CoreModel):
    MENU_TYPE_CHOICES = (
        (0, "目录"),
        (1, "菜单"),
        (2, "按钮"),
    )
    METHOD_CHOICE = (
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('PATCH', 'PATCH'),
        ('DELETE', 'DELETE'),
        ('HEAD', 'HEAD'),
        ('OPTIONS', 'OPTIONS'),
        ('TRACE', 'TRACE'),
    )
    name = fields.CharField(null=False, max_length=64, verbose_name="菜单名称")
    icon = fields.CharField(max_length=64, verbose_name="菜单图标")
    orderNum = fields.IntegerField(verbose_name="显示排序")
    menuType = fields.IntegerField(choices=MENU_TYPE_CHOICES, verbose_name="菜单类型")
    status = fields.BooleanField(default=False, verbose_name="菜单状态")
    visible = fields.BooleanField(default=False, verbose_name="显示状态")
    isFrame = fields.BooleanField(default=False, verbose_name="是否外链")
    web_path = fields.CharField(max_length=128, verbose_name="前端路由地址")
    component_path = fields.CharField(max_length=128, verbose_name="组件路径")
    interface_path = fields.CharField(max_length=256, verbose_name="接口路径")
    interface_method = fields.CharField(choices=METHOD_CHOICE, max_length=16, verbose_name="接口请求方式")
    isCache = fields.BooleanField(default=False, verbose_name="是否外链")
    parentId = fields.ForeignKey(to='Menu', on_delete=SET_DEFAULT, default=False, verbose_name="上级菜单")

    class Meta:
        verbose_name = '菜单管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"

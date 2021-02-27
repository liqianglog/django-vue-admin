from django.db.models import IntegerField, ForeignKey, CharField, CASCADE

from apps.op_drf.models import CoreModel


class Menu(CoreModel):
    # MENU_TYPE_CHOICES = (
    #     ("0", "目录"),
    #     ("1", "菜单"),
    #     ("2", "按钮"),
    # )
    # METHOD_CHOICE = (
    #     ('GET', 'GET'),
    #     ('POST', 'POST'),
    #     ('PUT', 'PUT'),
    #     ('PATCH', 'PATCH'),
    #     ('DELETE', 'DELETE'),
    #     ('HEAD', 'HEAD'),
    #     ('OPTIONS', 'OPTIONS'),
    #     ('TRACE', 'TRACE'),
    # )
    parentId = ForeignKey(to='Menu', on_delete=CASCADE, verbose_name="上级菜单", null=True, blank=True, )
    menuType = CharField(max_length=8, verbose_name="菜单类型")
    icon = CharField(max_length=64, verbose_name="菜单图标", null=True, blank=True)
    name = CharField(max_length=64, verbose_name="菜单名称")
    orderNum = IntegerField(verbose_name="显示排序")
    isFrame = CharField(max_length=8, verbose_name="是否外链")
    web_path = CharField(max_length=128, verbose_name="前端路由地址", null=True, blank=True)
    component_path = CharField(max_length=128, verbose_name="前端组件路径", null=True, blank=True)
    interface_path = CharField(max_length=256, verbose_name="后端接口路径", null=True, blank=True)
    interface_method = CharField(max_length=16, default='GET', verbose_name="接口请求方式")
    perms = CharField(max_length=256, verbose_name="权限标识", null=True, blank=True)
    status = CharField(max_length=8, verbose_name="菜单状态")
    visible = CharField(max_length=8, verbose_name="显示状态")
    isCache = CharField(max_length=8, verbose_name="是否缓存")

    class Meta:
        verbose_name = '菜单管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"

from django.core.cache import cache
from django.db.models import IntegerField, ForeignKey, CharField, CASCADE, Q

from application import settings
from apps.vadmin.op_drf.models import CoreModel


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
    parentId = ForeignKey(to='Menu', on_delete=CASCADE, verbose_name="上级菜单", null=True, blank=True, db_constraint=False)
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

    @classmethod
    def get_interface_dict(cls):
        """
        获取所有接口列表
        :return:
        """
        try:
            interface_dict = cache.get('permission_interface_dict', {}) if getattr(settings, "REDIS_ENABLE",
                                                                                   False) else {}
        except:
            interface_dict = {}
        if not interface_dict:
            for ele in Menu.objects.filter(~Q(interface_path=''), ~Q(interface_path=None), status='1', ).values(
                    'interface_path', 'interface_method'):
                if ele.get('interface_method') in interface_dict:
                    interface_dict[ele.get('interface_method', '')].append(ele.get('interface_path'))
                else:
                    interface_dict[ele.get('interface_method', '')] = [ele.get('interface_path')]
            if getattr(settings, "REDIS_ENABLE", False):
                cache.set('permission_interface_dict', interface_dict, 84600)
        return interface_dict

    @classmethod
    def delete_cache(cls):
        """
        清空缓存中的接口列表
        :return:
        """
        if getattr(settings, "REDIS_ENABLE", False):
            cache.delete('permission_interface_dict')

    class Meta:
        verbose_name = '菜单管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"

import logging

from django.core.management.base import BaseCommand
from django.db import connection
from django_tenants.utils import get_tenant_model, tenant_context

from application import settings
from dvadmin_tenants.models import Client

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    项目初始化命令: python manage.py init
    """

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        self.reset = False
        super().__init__(stdout, stderr, no_color, force_color)

    def add_arguments(self, parser):
        parser.add_argument('init_name', nargs='*', type=str, )
        parser.add_argument('-y', nargs='*')
        parser.add_argument('-Y', nargs='*')
        parser.add_argument('-n', nargs='*')
        parser.add_argument('-N', nargs='*')

    def run(self):
        INSTALLED_APPS = ['dvadmin.system'] + settings.INSTALLED_APPS
        # 初始化角色
        for app in sorted(list(set(INSTALLED_APPS)), key=INSTALLED_APPS.index):
            # 把不在 public 租户的不执行对应初始化方法
            if connection.tenant.schema_name == 'public' and app not in settings.SHARED_APPS:
                continue
            elif connection.tenant.schema_name != 'public' and app not in settings.TENANT_APPS:
                continue
            try:
                exec(f"""
from {app}.fixtures.initialize import Initialize
Initialize(reset={self.reset},app="{app}").run()
                """)
            except ModuleNotFoundError:
                pass
        print("初始化数据完成！")

    def init_public(self):
        from dvadmin_tenants.models import Client, Domain
        tenant, _ = Client.objects.get_or_create(id=100000, schema_name='public', name='超级租户', paid_until='2099-12-31',
                                                 on_trial=True)
        domain = Domain()
        domain.domain = 'public.django-vue-admin.com'  # don't add your port or www here!
        domain.tenant = tenant
        domain.is_primary = True
        domain.save()

    def handle(self, *args, **options):

        if isinstance(options.get('y'), list) or isinstance(options.get('Y'), list):
            self.reset = True
        if isinstance(options.get('n'), list) or isinstance(options.get('N'), list):
            self.reset = False
        print(f"正在准备初始化数据，{'如有初始化数据，将会不做操作跳过' if not self.reset else '初始数据将会先删除后新增'}...")
        if Client.objects.filter(schema_name='public', domains__isnull=False).count() == 0:
            print("超级租户不存在，正在创建中...")
            self.init_public()
        for tenant in get_tenant_model().objects.all():
            settings.INITIALIZE_RESET_LIST = []
            print(f"[{tenant.name}] 开始执行初始化数据！")
            with tenant_context(tenant):
                self.run()
            print(f"[{tenant.name}] 完成数据初始化！")

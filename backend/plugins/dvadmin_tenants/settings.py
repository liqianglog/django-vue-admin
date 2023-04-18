from application import settings

_SHARED_APPS = [
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'dvadmin.system',
    "drf_yasg",
    'captcha',
    'django_tenants',
    'dvadmin_tenants',
    'tenant_schemas_celery',
    'psqlextra'
]

# ================================================= #
# ***************** 插件配置区开始 *******************
# ================================================= #
# 路由配置
plugins_url_patterns = [
    {"re_path": r'api/tenant/', "include": "dvadmin_tenants.urls"}
]
# app 配置
apps = ['django_tenants', 'tenant_schemas_celery', 'django_celery_beat', 'django_celery_results', 'dvadmin_celery',
        'dvadmin_tenants', 'psqlextra']
if 'rest_framework_simplejwt.token_blacklist' in settings.INSTALLED_APPS:
    apps.append('rest_framework_simplejwt.token_blacklist')
# 租户模式中，public模式共享app配置
tenant_shared_apps = apps
# 租户独享app，只在普通租户有
exclusive_apps = []
# 中间件
middleware = [{
    "name": "django_tenants.middleware.main.TenantMainMiddleware",
    "sort": 0
}]
# 认证信息
authentication_backends = [{
    "name": "dvadmin_tenants.backends.TenantCustomBackend",
    "sort": 0
}]
# ================================================= #
# ***************** 插件配置区结束 *******************
# ================================================= #
settings.POSTGRES_EXTRA_DB_BACKEND_BASE = "django_tenants.postgresql_backend"
# ********** 创建路由 DATABASE_ROUTERS **********
settings.DATABASE_ROUTERS = ['django_tenants.routers.TenantSyncRouter', ] + list(
    getattr(settings, 'DATABASE_ROUTERS', []))
settings.DATABASE_ROUTERS = sorted(list(set(settings.DATABASE_ROUTERS)), key=settings.DATABASE_ROUTERS.index)

# ******************* 中间件 *****************
_MIDDLEWARE = list(getattr(settings, 'MIDDLEWARE', []))
for ele in middleware:
    _MIDDLEWARE.insert(ele.get('sort'), ele.get('name'))
MIDDLEWARE = sorted(list(set(_MIDDLEWARE)), key=_MIDDLEWARE.index)

# ********** 添加登录认证 **********
_AUTHENTICATION_BACKENDS = list(getattr(settings, 'AUTHENTICATION_BACKENDS', []))
for ele in authentication_backends:
    _AUTHENTICATION_BACKENDS.insert(ele.get('sort'), ele.get('name'))
AUTHENTICATION_BACKENDS = sorted(list(set(_AUTHENTICATION_BACKENDS)), key=_AUTHENTICATION_BACKENDS.index)

# ********** APPS管理 **********
if not hasattr(settings, 'TENANT_SHARED_APPS'):
    settings.TENANT_SHARED_APPS = []
if not hasattr(settings, 'TENANT_EXCLUSIVE_APPS'):
    settings.TENANT_EXCLUSIVE_APPS = []
settings.TENANT_SHARED_APPS += tenant_shared_apps  # 共享apps, 表不在普通租户建，读取表默认走public的表
settings.TENANT_EXCLUSIVE_APPS += exclusive_apps  # 独享apps
_INSTALLED_APPS = list(set(_SHARED_APPS))
for ele in settings.INSTALLED_APPS + apps:
    _INSTALLED_APPS.append(ele)
_INSTALLED_APPS = sorted(list(set(_INSTALLED_APPS)), key=_INSTALLED_APPS.index)

# # 租户 APPS
_TENANT_APPS = list(set(getattr(settings, 'TENANT_APPS', _INSTALLED_APPS)))

_SHARED_APPS = list(set(_SHARED_APPS + settings.TENANT_SHARED_APPS))
# 租户独享app，只在普通租户有
for ele in settings.TENANT_EXCLUSIVE_APPS:
    if ele in _SHARED_APPS:
        _SHARED_APPS.remove(ele)

# 租户共享apps, 表不在普通租户建，读取表默认走public的表
for ele in settings.TENANT_SHARED_APPS:
    if ele in _TENANT_APPS:
        _TENANT_APPS.remove(ele)

settings.SHARED_APPS = _SHARED_APPS
settings.TENANT_APPS = _TENANT_APPS
settings.INSTALLED_APPS = _INSTALLED_APPS
# ********** 注册路由 **********
settings.PLUGINS_URL_PATTERNS += plugins_url_patterns

# ********** 日志 **********
_LOGGING = settings.LOGGING
_LOGGING["filters"] = {
    'tenant_context': {
        '()': 'django_tenants.log.TenantContextFilter'
    }
}
TENANT_LOG_FORMAT = '[%(schema_name)s:%(domain_url)s][%(asctime)s][%(name)s.%(funcName)s():%(lineno)d] [%(levelname)s] %(message)s'
_LOGGING["handlers"]["console"]["filters"] = ['tenant_context']
_LOGGING["handlers"]["console"]["formatter"] = 'tenant_context'
LOGGING_FORMATTERS = _LOGGING["formatters"]
LOGGING_FORMATTERS["tenant_context"] = {
    'format': TENANT_LOG_FORMAT,
    'datefmt': '%Y-%m-%d %H:%M:%S',
}
_LOGGING["formatters"] = LOGGING_FORMATTERS
settings.LOGGING = _LOGGING

# ********** 设置租户和域模型所在的位置 **********
settings.TENANT_MODEL = "dvadmin_tenants.Client"  # app.Model
settings.TENANT_DOMAIN_MODEL = "dvadmin_tenants.Domain"  # app.Model

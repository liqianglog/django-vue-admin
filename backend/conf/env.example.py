# ================================================= #
# *************** mysql数据库 配置  *************** #
# ================================================= #
# 数据库地址
DATABASE_ENGINE = "django.db.backends.mysql"
# 数据库地址 改为自己数据库地址
DATABASE_HOST = "127.0.0.1"
# # 数据库端口
DATABASE_PORT = 3306
# # 数据库用户名
DATABASE_USER = "root"
# # 数据库密码
DATABASE_PASSWORD = "123456"
# 数据库名
DATABASE_NAME = "database_name"

# 表前缀
TABLE_PREFIX = "sys_"
APP_PREFIX = "app_"
# ================================================= #
# ******** redis配置，无redis 可不进行配置  ******** #
# ================================================= #
# REDIS_PASSWORD = ''
# REDIS_HOST = '127.0.0.1'
# REDIS_URL = f'redis://:{REDIS_PASSWORD or ""}@{REDIS_HOST}:6380'
# ================================================= #
# ****************** 功能 启停  ******************* #
# ================================================= #
DEBUG = False
# 是否启用插件，不需要可以设置为False
ENABLE_PLUGINS = False
# 启动登录详细概略获取(通过调用api获取ip详细地址)
ENABLE_LOGIN_ANALYSIS_LOG = True
# 是否启用登录验证码，不需要可以设置为False
CAPTCHA_STATE = False
# 登录接口 /api/token/ 是否需要验证码认证，用于测试，正式环境建议取消
LOGIN_NO_CAPTCHA_AUTH = True
# ================================================= #
# ****************** 其他 配置  ******************* #
# ================================================= #

ALLOWED_HOSTS = ["*"]

# 默认密码
DEFAULT_PASSWORD = "admin123456"

# 初始化需要执行的列表，用来初始化后执行
INITIALIZE_LIST = []
INITIALIZE_RESET_LIST = []

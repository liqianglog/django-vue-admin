
# ================================================= #
# ************** mysql数据库 配置  ************** #
# ================================================= #
# 数据库类型 MYSQL/SQLITE3
DATABASE_TYPE = "MYSQL"
# 数据库地址
DATABASE_HOST = "127.0.0.1"
# 数据库端口
DATABASE_PORT = 3306
# 数据库用户名
DATABASE_USER = "root"
# 数据库密码
DATABASE_PASSWORD = "q1w2e3r4T%Y^U&MYSQL"
# 数据库名
DATABASE_NAME = "django-vue-admin"

# ================================================= #
# ************** redis 数据库配置  ************** #
# ================================================= #
# 是否启用Redis缓存
# 注：不使用redis则无法使用celery
REDIS_ENABLE = True
REDIS_DB = 1
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = 'q1w2e3r4T%Y^U&'
# celery 定时任务redis 库号
CELERY_DB = 2

# ================================================= #
# ************** 默认配置  ************** #
# ================================================= #
# 只允许访问的ip地址列表
ALLOWED_HOSTS = ['*']
# 允许跨域源
CORS_ORIGIN_ALLOW_ALL = True
# 允许ajax请求携带cookie
CORS_ALLOW_CREDENTIALS = False
# 验证码状态
CAPTCHA_STATE = True
# 操作日志配置
API_LOG_ENABLE = True
API_LOG_METHODS = ['POST', 'DELETE', 'PUT'] # 'ALL' or ['POST', 'DELETE']
# 接口权限
INTERFACE_PERMISSION = True
# 是否开启登录ip转换成城市位置
ENABLE_LOGIN_LOCATION = True

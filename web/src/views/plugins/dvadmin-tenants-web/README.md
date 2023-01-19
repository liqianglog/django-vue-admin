# dvadmin-tenants-web
dvadmin-tenants-web 是 dvadmin的一款租户前端插件


## 后端 dvadmin-tenants 介绍
dvadmin-tenants 是 dvadmin的一款租户插件，集成 `tenant-schemas-celery`、`django-tenants`、`django-postgres-extra` 模块，数据库采用 PostgreSQL (mysql无法兼容此插件) ，实现了多租户的saas模式，

解决多租户问题通常有三种解决方案。
1. 隔离方法：单独的数据库。每个租户都有自己的数据库。
2. 半隔离方法：共享数据库，独立模式。所有租户一个数据库，但每个租户一个模式。
3. 共享方法：共享数据库、共享模式。所有租户共享相同的数据库和模式。有一个主租户表，所有其他表都有一个指向的外键。

此插件实现了第二种方法，在我们看来，它代表了简单性和性能之间的理想折衷。



# 重要说明

1. 数据库需要从MySQL 换成 PostgreSQL；
2. 如果需要使用本插件，建议新建数据库后，再进行迁移旧数据；
3. 详细后端文档可阅读 [django-tenants](https://django-tenants.readthedocs.io/en/latest/) 官网文档；
4. 多租户需要通过`子域名`的方式进行区分，如需要通过`子路径`方式进行区分，请参考 https://django-tenants.readthedocs.io/en/latest/install.html#sub-folder-support (未进行试验，请自行二开)
5. 数据库迁移时，与正常的dvadmin 迁移、初始化有所区别，请参考下面迁移数据



#安装配置说明

### 安装

使用pip安装软件包：

```python
pip install dvadmin-tenants
```

#### 方式一: 一键导入注册配置

在 application / settings.py 插件配置中下导入默认配置

~~~
...
from dvadmin_tenants.settings import * # 租户插件(建议放最后)
~~~

#### 方式二: 参考 dvadmin_tenants/settings.py 自行阅读注册



### 修改数据库配置

修改`conf/env.py`下的数据库配置引擎为 `psqlextra.backend`

~~~
# 数据库引擎
DATABASE_ENGINE = "psqlextra.backend"
# 数据库地址 改为自己数据库地址
DATABASE_HOST = "127.0.0.1"
# 数据库端口
DATABASE_PORT = 5432
# 数据库用户名
DATABASE_USER = "postgres"
# 数据库密码
DATABASE_PASSWORD = "123456"
# 数据库名
DATABASE_NAME = "dvadmin"
~~~



### 迁移数据

与正常的dvadmin 迁移有所区别

~~~python
python3 manage.py pgmakemigrations 
python3 manage.py migrate_schemas 
# 注意备份初始化信息
python3 manage.py tenant_init
~~~

### 修改host文件

通过修改电脑 hosts (自行百度) ，把域名 `public.django-vue-admin.com` (可自行更改数据库配置) 映射成`127.0.0.1` ip地址



### 打开项目

通过修改hosts后，通过浏览器进行打开

后端：http://public.django-vue-admin.com:8000

前端： http://public.django-vue-admin.com:8080 

账号密码：dvadmin默认



## 常用配置

#### 1. 添加共享app

共享：只在超级租户public中建表，表不在普通租户建，读取表默认走public的表

在 settings.py 下，添加如下配置

```python
INSTALLED_APPS = [ # 正常注册app
  ...
  '共享app名'
]
TENANT_SHARED_APPS = [ #　配置独享
  ...
  '共享app名'
]
```

#### 2. 添加独享app

独享：除超级租户public外的所有模式都会建立对应表(只在普通租户建立表)

在 settings.py 下，添加如下配置

~~~python
INSTALLED_APPS = [ # 正常配置app
  ...
  '独享app名'
]
TENANT_EXCLUSIVE_APPS = [ # 配置共享
  ...
  '独享app名'
]
~~~

#### 3. 添加通用app

通用：正常注册app 即可，默认会在超级租户及普通租户都会建立表

~~~python
INSTALLED_APPS = [ # 正常配置app
  ...
  '通用app名'
]
~~~

#### 4. 配置超级租户

4.1 初始化后通过数据库表中，`public` 模式下的 `sys_tenant_domain` 表手动进行修改 domain 字段。

4.2 通过修改电脑 host ，把域名 `public.django-vue-admin.com` (可自行更改数据库配置) 映射成`127.0.0.1` ip地址



# 使用说明

通过安装租户前端插件，在页面上进行租户创建建立。

![](https://bbs.django-vue-admin.com/uploads/20221126/aefb65e0dfa3348d818b4a9bf24382f1.png)

![](https://bbs.django-vue-admin.com/uploads/20221126/79eb651a9fb7a0c18fb8dc81a0201445.png)

![](https://bbs.django-vue-admin.com/uploads/20221126/45a77721cc35b31b3002ac4eef48ee62.png)

![](https://bbs.django-vue-admin.com/uploads/20221126/050f5190d6f716a300aa11a75e13d4d3.png)


通过修改hosts ，访问子租户域名信息。

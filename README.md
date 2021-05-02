# Django-Vue-Admin

[![img](https://img.shields.io/badge/license-MIT-blue.svg)](https://gitee.com/liqianglog/django-vue-admin/blob/master/LICENSE) [![img](https://img.shields.io/pypi/v/django-simpleui.svg)](https://pypi.org/project/django-simpleui/#history) [![img](https://img.shields.io/badge/python-%3E=3.6.x-green.svg)](https://python.org/)  ![PyPI - Django Version badge](https://img.shields.io/badge/django%20versions-2.2-blue)![img](https://img.shields.io/badge/node-%3E%3D%2012.0.0-brightgreen)



## 平台简介

Django-Vue-Admin 是一套全部开源的快速开发平台，毫无保留给个人及企业免费使用。

* 前端采用ruoyi-ui 、Vue、Element UI。
* 后端采用Python语言Django框架。
* 权限认证使用Jwt，支持多终端认证系统。
* 支持加载动态权限菜单，多方式轻松权限控制。
* 特别鸣谢：<u>[Gin-Vue-Admin](https://www.gin-vue-admin.com/)</u>，[RuoYi](https://gitee.com/y_project/RuoYi-Vue) ，[Vue-Element-Admin](https://github.com/PanJiaChen/vue-element-admin)，[eladmin-web](https://gitee.com/elunez/eladmin-web?_from=gitee_search)。

## QQ群

- QQ群号：812482043

- 二维码

  <img src='https://gitee.com/liqianglog/django-vue-admin/raw/master/dvadmin-ui/src/assets/images/qq.jpg' width='200'>

## 源码地址

gitee地址(主推)：[https://gitee.com/liqianglog/django-vue-admin](https://gitee.com/liqianglog/django-vue-admin)

github地址：[https://github.com/liqianglog/django-vue-admin](https://github.com/liqianglog/django-vue-admin)

## 内置功能

##### 后期版本 [版本功能说明](https://gitee.com/liqianglog/django-vue-admin/wikis/releaseNote?sort_id=3615540)

1.  用户管理：用户是系统操作者，该功能主要完成系统用户配置。
2.  部门管理：配置系统组织机构（公司、部门、小组），树结构展现支持数据权限。
3.  岗位管理：配置系统用户所属担任职务。
4.  菜单管理：配置系统菜单，操作权限，按钮权限标识、后端接口权限等。
5.  角色管理：角色菜单权限分配、数据权限分配、设置角色按机构进行数据范围权限划分。
6.  字典管理：对系统中经常使用的一些较为固定的数据进行维护。
7.  参数管理：对系统动态配置常用参数。
8.  文件管理：管理所有上传的和导出的文件。
9.  通知公告：发布通知公告给所有人，进行消息的通知。
10.  操作日志：系统正常操作日志记录和查询；系统异常信息日志记录和查询。
11.  登录日志：系统登录日志记录查询包含登录异常。
12.  定时日志：celery定时任务执行日志记录。
13.  在线用户：当前系统中活跃用户状态监控、用户强退功能。
14.  定时任务：在线（添加、修改、删除)任务调度包含执行结果日志。
15.  在线构建器：拖动表单元素生成相应的HTML代码。

## 在线体验

演示地址：[http://demo.django-vue-admin.com/](http://demo.django-vue-admin.com/) 账号：admin 密码：123456

文档地址：[http://django-vue-admin.com/](http://django-vue-admin.com/)

## 前端

### 	开发

```bash
# 克隆项目
git clone https://gitee.com/liqianglog/django-vue-admin.git

# 进入项目目录
cd dvadmin-ui

# 安装依赖
npm install --registry=https://registry.npm.taobao.org

# 启动服务
npm run dev

# 浏览器访问 http://localhost:8080
# .env.development 文件中可配置启动端口等参数
```

### 	发布

```bash
# 构建测试环境
npm run build:stage

# 构建生产环境
npm run build:prod
```

## 后端

~~~bash
1. 进入项目目录 cd dvadmin-backend
2. 在项目根目录中，复制 ./conf/env.example.py 文件为一份新的到 ./conf 文件夹下，并重命名为 env.py

3. 在 env.py 中配置数据库信息
	mysql数据库版本建议:5.7以上
	mysql数据库字符集：utf8mb4
	mysql数据库排序规则：utf8mb4_0900_ai_ci
	
4. 安装依赖环境
	pip3 install -r requirements.txt
5. 执行迁移命令：
	python3 manage.py makemigrations
	python3 manage.py migrate
6. 初始化数据
	python3 manage.py init
7. 启动项目
	python3 manage.py runserver 127.0.0.1:8000

定时任务启动命令：
	celery -A application  worker -B --loglevel=info
注：
	Windows 运行celery 需要安装 pip install eventlet
	celery -A application  worker -P eventlet --loglevel=info

初始账号：admin 密码：123456

后端接口文档地址：http://127.0.0.1:8000/docs/
~~~

### docker-compose 运行

~~~shell
# 先安装docker-compose (自行百度安装),执行此命令等待安装
docker-compose up
# 初始化后端数据(第一次执行即可)
docker exec -ti dvadmin-django bash
python manage.py init -y
exit

前端地址：http://127.0.0.1:8080
后端地址：http://127.0.0.1:8000
账号：admin 密码：123456
~~~



## 演示图

<table>
    <tr>
        <td><img src="https://oscimg.oschina.net/oscnet/cd1f90be5f2684f4560c9519c0f2a232ee8.jpg"/></td>
        <td><img src="https://oscimg.oschina.net/oscnet/1cbcf0e6f257c7d3a063c0e3f2ff989e4b3.jpg"/></td>
    </tr>
    <tr>
        <td><img src="https://oscimg.oschina.net/oscnet/707825ad3f29de74a8d6d02fbd73ad631ea.jpg"/></td>
        <td><img src="https://oscimg.oschina.net/oscnet/46be40cc6f01aa300eed53a19b5012bf484.jpg"/></td>
    </tr>
    <tr>
        <td><img src="https://oscimg.oschina.net/oscnet/4284796d4cea240d181b8f2201813dda710.jpg"/></td>
        <td><img src="https://oscimg.oschina.net/oscnet/3ecfac87a049f7fe36abbcaafb2c40d36cf.jpg"/></td>
    </tr>
	<tr>
        <td><img src="https://oscimg.oschina.net/oscnet/71c2d48905221a09a728df4aff4160b8607.jpg"/></td>
        <td><img src="https://oscimg.oschina.net/oscnet/c14c1ee9a64a6a9c2c22f67d43198767dbe.jpg"/></td>
    </tr>	 
    <tr>
        <td><img src="https://oscimg.oschina.net/oscnet/5e8c387724954459291aafd5eb52b456f53.jpg"/></td>
        <td><img src="https://oscimg.oschina.net/oscnet/644e78da53c2e92a95dfda4f76e6d117c4b.jpg"/></td>
    </tr>
	<tr>
        <td><img src="https://oscimg.oschina.net/oscnet/fdea1d8bb8625c27bf964176a2c8ebc6945.jpg"/></td>
        <td><img src="https://oscimg.oschina.net/oscnet/509d2708cfd762b6e6339364cac1cc1970c.jpg"/></td>
    </tr>
	<tr>
        <td><img src="https://oscimg.oschina.net/oscnet/up-f1fd681cc9d295db74e85ad6d2fe4389454.png"/></td>
        <td><img src="https://oscimg.oschina.net/oscnet/up-c195234bbcd30be6927f037a6755e6ab69c.png"/></td>
    </tr>
</table>

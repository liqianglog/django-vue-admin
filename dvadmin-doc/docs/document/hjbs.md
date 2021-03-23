# 环境部署
## 1.前端搭建环境

### 1.1 安装node

## 1. 后端搭建环境

### 1.1 安装Python3.8

### 1.2 安装Reids
        sudo apt-get install -y redis-server

### 1.3 安装nginx
        sudo apt-get install -y nginx

### 1.1 安装其它软件
        sudo apt-get install -y python3-venv pcre pcre-devel pcre-static zlib* gcc openssl openssl-devel libffi-devel 

## 2. 创建虚拟环境
### 2.1 进入项目目录 cd gh-baohua-backend
        在项目根目录中，复制./conf/env.example.py文件为一份新的到./conf文件夹下，并重命名为env.py，在env.py中配置数据库信息。

### 2.2 激活虚拟环境

#### 2.2.1 python(python3) -m venv xxxx-venv, (xxxx根据情况定义)

#### 2.2.2 \xxxx-venv\Scripts\activate (window OS)

#### 2.2.3 sudo chmod -R 777 xxxx-venv/* (Linux OS)
#### 2.2.4 source ./gh-baohua-venv/bin/activate (Linux OS)

## 3. 升级pip

	sudo python(python3) -m pip install --upgrade pip

## 4. 安装依赖环境

	pip install -r requirements.txt

## 5. 执行迁移命令：
	python manage.py makemigrations
	python manage.py migrate

## 6. 初始化数据
	python manage.py init

## 7. 启动项目
	python manage.py runserver 8888

## 8. 初始账号:admin  密码:123456

## 9. 搭建正式环境，完成上述步骤1-6

### 9.1 配置uwsgi.ini(主要配置项)

[uwsgi]

chdir           = /mnt/dvadmin-backend
wsgi-file       = /mnt/dvadmin-backend/application/wsgi.py
home            = /mnt/dvadmin-backend/leo-baohua-venv
pidfile = /mnt/dvadmin-backend/uwsgi.pid
daemonize = /mnt/dvadmin-backend/uwsgi.log
master          = true
processes       = 8
socket          = 0.0.0.0:7777
module          = application.wsgi:application
vacuum          = true

### 9.2 Nginx 配置

#### 9.2.1 配置uwsgi
        server {
                listen 7077;
                server_name 192.168.xx.xxx;
    
                location / {
                        include uwsgi_params;
                        uwsgi_pass 127.0.0.1:7777;
                }
        }

#### 9.2.2 配置前端
        server {
                listen 7078;
                server_name 192.168.xx.xxx;
    
                root /mnt/dvadmin-ui/dist;
    
                index index.html index.htm index.nginx-debian.html;
    
                location / {
                        try_files $uri $uri/ /index.html;
                }
        }

#### 9.2.3 配置前端接口-env.production
VUE_APP_BASE_API = 'http://192.168.xx.xxx:7077'


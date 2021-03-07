#!/bin/bash
###   init            初始化项目
###   start           启动项目
###   stop            停止项目
###   restart         重启项目
###   -h               显示帮助信息.
help() {
	awk -F'### ' '/^###/ { print $2 }' "$0"
}

if [[ $# == 0 ]] || [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
	help
	exit 1
fi

#初始化方法
init(){
    echo "正在初始化中..."
    sudo find . -path "*/*/*/migrations/*.py" -not -name "__init__.py" -delete
    sudo rm -rf docker_env/mysql/data
    python ./manage.py initialization
    echo "初始化完成..."
}

#启动方法
start(){
    echo "正在启动中..."
    docker-compose up
    echo "启动完成..."
}

case "$1" in

    init)
        echo "=== init "
        init
        start
        ;;
    start)
        echo "=== start ";;

    stop)
        echo "=== stop ";;

    restart)
        echo "=== restart ";;

    *)
        help
	      exit 1

esac

FROM python:3.8.10-slim-buster
WORKDIR /backend
COPY ./backend/ .
RUN awk 'BEGIN { cmd="cp -i ./conf/env.example.py   ./conf/env.py "; print "n" |cmd; }'
RUN    sed -i s@archive.debian.com@mirrors.aliyun.com@g /etc/apt/sources.list && \
  sed -i s@security.debian.org@mirrors.aliyun.com@g /etc/apt/sources.list && \
  sed -i s@deb.debian.org@mirrors.aliyun.com@g /etc/apt/sources.list
RUN apt update && apt-get install -y  default-libmysqlclient-dev gcc
RUN python3 -m pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
CMD ["/backend/docker_start.sh"]

FROM python:3.7
# ENV PYTHONUNBUFFERED 1
RUN sed -i s/deb.debian.org/mirrors.163.com/g /etc/apt/sources.list
RUN cat /etc/apt/sources.list
RUN apt-get clean
RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y python3.7-dev libpq-dev libopencv-dev python-opencv
RUN apt-get install -y redis-tools
RUN mkdir /dvadmin-backend
WORKDIR /dvadmin-backend
COPY ./dvadmin-backend/requirements.txt /
COPY ./dvadmin-backend/conf/env.example.py /dvadmin-backend/conf/env.py
RUN python3 -m pip install -i https://mirrors.aliyun.com/pypi/simple/ -r /requirements.txt
RUN python3 -m pip install -i https://mirrors.aliyun.com/pypi/simple/ uwsgi==2.0.19.1
CMD ["/dvadmin-backend/docker_start.sh"]
# ENTRYPOINT [ "uwsgi --ini /backend/azcrm/uwsgi.ini" ]

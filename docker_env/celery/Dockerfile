FROM python:3.8
# ENV PYTHONUNBUFFERED 1
RUN sed -i s/deb.debian.org/mirrors.163.com/g /etc/apt/sources.list
RUN cat /etc/apt/sources.list
RUN apt-get clean
RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y python3.8-dev libpq-dev libopencv-dev
RUN apt-get install -y redis-tools
RUN mkdir /dvadmin-backend
WORKDIR /dvadmin-backend
COPY ./dvadmin-backend/requirements.txt /
COPY ./dvadmin-backend/conf/env.example.py /dvadmin-backend/conf/env.py
RUN python3 -m pip install -i https://mirrors.aliyun.com/pypi/simple/ -r /requirements.txt
CMD ["celery", "-A", "application", "worker", "-B", "--loglevel=info"]


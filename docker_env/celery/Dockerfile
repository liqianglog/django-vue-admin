FROM python:3.7
# ENV PYTHONUNBUFFERED 1
# RUN sed -i s/deb.debian.org/mirrors.163.com/g /etc/apt/sources.list
# RUN cat /etc/apt/sources.list 
# RUN apt-get clean
RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y python3.7-dev libpq-dev libopencv-dev python-opencv
RUN apt-get install -y redis-tools 

COPY ./docker_env/celery/requirement.txt /
RUN mkdir /backend
WORKDIR /backend
RUN python3.7 -m pip install -i https://mirrors.aliyun.com/pypi/simple/ -r /requirement.txt --use-feature=2020-resolver
CMD ["celery", "-A", "azcrm", "worker", "-B", "--loglevel=info"]


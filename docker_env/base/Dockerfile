# pull official base image
FROM  python:3.9-buster
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
#RUN sed -i s/deb.debian.org/mirrors.163.com/g /etc/apt/sources.list
RUN cat /etc/apt/sources.list
RUN apt-get clean
RUN apt-get update
#RUN apt -y update
#RUN apt -y upgrade

#RUN apt-get install -y build-essential
# set work directory
WORKDIR /code

# set environment variables
ENV PYTHONPATH /code
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV DOCKERIZED 1
RUN echo 'DOCKERIZED=' DOCKERIZED  # 使用不同的配置
# install dependencies
RUN python -m pip install -i https://mirrors.aliyun.com/pypi/simple/ --upgrade pip
# 工作目录
COPY ./backend/ /code

RUN #apt install ./google-chrome-stable_current_amd64.deb

RUN python -m pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
RUN python -m pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements_add.txt

# copy entrypoint.sh
COPY ./backend/docker-entrypoint.sh /docker-entrypoint.sh

# run entrypoint.sh
EXPOSE 8000
RUN chmod +x /docker-entrypoint.sh
CMD /bin/bash /docker-entrypoint.sh

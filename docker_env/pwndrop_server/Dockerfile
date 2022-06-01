# pull official base image
FROM  debian:unstable-slim

# set work directory
WORKDIR /code
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
#RUN sed -i s/deb.debian.org/mirrors.163.com/g /etc/apt/sources.list
RUN cat /etc/apt/sources.list
RUN apt-get clean
RUN apt-get update
RUN apt-get install -y procps

# copy code
COPY ./docker_env/pwndrop_server/pwndrop-linux-amd64.tar.gz /code

# copy entrypoint.sh
COPY ./docker_env/pwndrop_server/docker-entrypoint.sh /code/docker-entrypoint.sh

# run entrypoint.sh
EXPOSE 8000
RUN chmod +x docker-entrypoint.sh
CMD /bin/bash docker-entrypoint.sh
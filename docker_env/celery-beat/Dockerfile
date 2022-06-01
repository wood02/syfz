# pull official base image
FROM  syfz_base:v1.0.1

# set work directory
WORKDIR /code

# copy code
COPY ./backend/ /code

# copy entrypoint.sh
COPY ./docker_env/celery-beat/docker-entrypoint.sh /docker-entrypoint.sh

# run entrypoint.sh
EXPOSE 8000
RUN chmod +x /docker-entrypoint.sh
CMD /bin/bash /docker-entrypoint.sh

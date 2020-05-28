FROM tiangolo/uwsgi-nginx-flask:python3.7
# tiangolo/uwsgi-nginx-flask:python3.7 is a community docker image. Which can
# be examined here https://github.com/tiangolo/uwsgi-nginx-flask-docker/blob/master/python3.6/Dockerfile
# Overall, there is an abstraction benefit to use such docker images Vs
# building Nginx & UWSGI from scratch and default configuration.
# Here are the key points of the above image:
# (ON RUN)
# 1 - There is a "entrypoint.sh" which provides a bash environment and
#     executes "start.sh". Both these files can be found at the above repo.
# 2 - "start.sh" executes "/app/prestart.sh" - This can be configured to run
#     some start-up process such as database migrations. Post execution
#     of "/app/prestart.sh" supervisord is executed; which in turn
#     starts up Nginx and uWSGI.

# (ENVIRONMENT - only key envvars mentioned)
# 3 - ENVVAR "UWSGI_INI" <- This points to the uwsgi.ini file, by default /app/uwsgi.ini.
# 4 - ENVVAR "LISTEN_PORT" <- This is the Nginx port, by default set to 80.
# 5 - ENVVAR "PYTHONPATH" <- By default set to /app.

LABEL MAINTAINER="Asif Ali<asifali22@github.com>"

ARG APP_DIR=/digi-srv
ARG SERVICE_NAME=digital_reporter
ARG LOG_DIR_PATH=/var/log/uwsgi

WORKDIR $APP_DIR

RUN apt-get update \
    && apt-get install --fix-missing -y ca-certificates gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install
RUN rm google-chrome-stable_current_amd64.deb

RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

ARG POETRY_VERSION=1.0.0

RUN pip install poetry==$POETRY_VERSION
RUN poetry --version
COPY poetry.lock pyproject.toml ${APP_DIR}/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY ./ ${APP_DIR}

ARG ENVIRONMENT=dev
RUN sed -n '/^[a-zA-Z]/p' ${APP_DIR}/.env-${ENVIRONMENT} | sed -e 's/\r//g' > ${APP_DIR}/.env
RUN rm ${APP_DIR}/.env-*

COPY prestart-nginx-uwsgi.sh /app/prestart.sh

RUN mkdir -p "${LOG_DIR_PATH}""${APP_DIR}"
VOLUME "${LOG_DIR_PATH}""${APP_DIR}"

# Build entrypoint.sh to create config files at runtime
# to consider ENV variables and BUILD ARGS.
RUN echo '#!/usr/bin/env bash' > /entrypoint.sh
RUN echo 'set -e' >> /entrypoint.sh
RUN echo 'export `cat'" ${APP_DIR}"'/.env | xargs`' >> /entrypoint.sh
RUN cat conf-webserver/nginx-build-conf.sh | grep -Ev "^#!|^set"          >> /entrypoint.sh
RUN cat conf-webserver/nginx-build-conf-service.sh | grep -Ev "^#!|^set"  >> /entrypoint.sh
RUN cat conf-webserver/uwsgi-build-ini.sh | grep -Ev "^#!|^set"           >> /entrypoint.sh
RUN cat conf-cron/uwsgi-cron-header.sh | grep -Ev "^#!|^set"              >> /entrypoint.sh
RUN cat conf-cron/uwsgi-reporter-cron.sh | grep -Ev "^#!|^set"            >> /entrypoint.sh
RUN echo 'exec "$@"' >> /entrypoint.sh
RUN chmod +x /entrypoint.sh


# Substitute build arguments at time of building Dockerfile.
# '@' is used as an alternative to '/' in s/.../.../g as '/' requries
# complex escaping when build args may contain '/' themselves.
# resulting in s@...@...@g.
RUN sed -i 's@${USE_APP_PATH}'"@${APP_DIR}"'@g' /entrypoint.sh
RUN sed -i 's@${USE_LOG_DIR_PATH}'"@${LOG_DIR_PATH}"'@g' /entrypoint.sh
RUN sed -i 's@${USE_SERVICE_NAME}'"@${SERVICE_NAME}"'@g' /entrypoint.sh
RUN sed -i -e 's/\r//g' /entrypoint.sh

ENV PYTHONPATH=./
ENV UWSGI_INI=${APP_DIR}/conf-webserver/uwsgi.ini

# tiangolo/uwsgi-nginx-flask:python3.6 now executes the following command
# [on-prompt] entrypoint.sh start.sh


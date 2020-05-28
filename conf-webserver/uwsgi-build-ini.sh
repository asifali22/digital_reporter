#!/usr/bin/env bash
set -e

USE_APP_PATH=${APP_DIR:-/zest-srv}
USE_SERVICE_NAME=${SERVICE_NAME:-digital_reporter}
USE_LOG_DIR_PATH=${LOG_DIR_PATH:-/var/log/uwsgi}
USE_UWSGI_PROCESSES=${UWSGI_PROCESSES:-4}

content='[uwsgi]\n'
content=$content"strict = true\n"
content=$content"die-on-term = true\n"
content=$content"need-app = true\n"
content=$content"chdir = ${USE_APP_PATH}\n"
content=$content"module = wsgi:application\n"
content=$content"logto = ${USE_LOG_DIR_PATH}${USE_APP_PATH}/${USE_SERVICE_NAME}.log\n"
content=$content'master = true\n'
content=$content'enable-threads = true\n'
content=$content'single-interpreter = true\n'
content=$content"processes = ${USE_UWSGI_PROCESSES}\n"
content=$content'vacuum = true\n'

# Save generated uwsgi.ini
printf "$content" | sed -e 's/\r//g' > ${USE_APP_PATH}/conf-webserver/uwsgi.ini


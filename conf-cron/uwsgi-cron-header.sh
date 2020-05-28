#!/usr/bin/env bash
set -e

USE_APP_PATH=${APP_PATH:-/digi-srv}

content='\n; cron configuration\n'

# append to generated uwsgi.ini
printf "$content" | sed -e 's/\r//g' >> ${USE_APP_PATH}/conf-webserver/uwsgi.ini


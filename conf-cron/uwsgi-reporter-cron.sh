#!/usr/bin/env bash
set -e

USE_APP_PATH=${APP_PATH:-/digi-srv}
USE_SERVICE_NAME=${SERVICE_NAME:-digital_reporter}
USE_LOG_DIR_PATH=${LOG_DIR_PATH:-/var/log/uwsgi}
USE_REPORTER_JOB_SCHEDULE_M=${REPORTER_JOB_SCHEDULE_M:--30}
USE_REPORTER_HARAKIRI=${REPORTER_JOB_HARAKIRI:-1740}

content="cron2 = minute=${USE_REPORTER_JOB_SCHEDULE_M},harakiri=${USE_REPORTER_HARAKIRI},unique=1 ${USE_APP_PATH}/conf-cron/reporter-cron.sh\n"

# append to generated uwsgi.ini
printf "$content" | sed -e 's/\r//g' >> ${USE_APP_PATH}/conf-webserver/uwsgi.ini

content='#!/usr/bin/env bash\n'
content=$content"cd ${USE_APP_PATH}\n"
content=$content"python cron/cron_run_reporter.py\n"

printf "$content" | sed -e 's/\r//g' > ${USE_APP_PATH}/conf-cron/reporter-cron.sh
chmod +x ${USE_APP_PATH}/conf-cron/reporter-cron.sh
#!/usr/bin/env bash
set -e

# Get the maximum upload file size for Nginx, default to 0: unlimited
USE_NGINX_MAX_UPLOAD=${NGINX_MAX_UPLOAD:-0}

# Get the number of workers for Nginx, default to 1
USE_NGINX_WORKER_PROCESSES=${NGINX_WORKER_PROCESSES:-1}

# Set the max number of connections per worker for Nginx, if requested
# Cannot exceed worker_rlimit_nofile, see NGINX_WORKER_OPEN_FILES below
USE_NGINX_MAX_WORKER_CONNECTIONS=${NGINX_MAX_WORKER_CONNECTIONS:-1024}

USE_NGINX_LOG_LEVEL=${NGINX_LOG_LEVEL:-info}
USE_NGINX_REWRITE_LOG=${NGINX_REWRITE_LOG:-off}

content='user  nginx;\n'
content=$content"worker_processes ${USE_NGINX_WORKER_PROCESSES};\n"
content=$content"error_log  /var/log/nginx/error.log ${USE_NGINX_LOG_LEVEL};\n"
content=$content'pid        /var/run/nginx.pid;\n'
content=$content'events {\n'
content=$content"    worker_connections ${USE_NGINX_MAX_WORKER_CONNECTIONS};\n"
content=$content'}\n'
content=$content'http {\n'
content=$content'    include       /etc/nginx/mime.types;\n'
content=$content'    default_type  application/octet-stream;\n'
content=$content'    log_format  primary  '"'[\$time_iso8601]|\$remote_addr|\$remote_user|\"\$request\"|'\n"
content=$content'                         '"'\$status|\$upstream_response_time(s)|\$body_bytes_sent|\"\$http_referer\"|'\n"
content=$content'                         '"'\"\$http_user_agent\"|\"\$http_x_forwarded_for\"';\n"
content=$content'    access_log  /var/log/nginx/access.log  primary;\n'
content=$content"    rewrite_log ${USE_NGINX_REWRITE_LOG};\n"
content=$content'    sendfile on;\n'
content=$content'    keepalive_timeout  65;\n'
content=$content'    include /etc/nginx/conf.d/*.conf;\n'
content=$content'}\n'
content=$content'daemon off;\n'

# Set the max number of open file descriptors for Nginx workers, if requested
if [ -n "${NGINX_WORKER_OPEN_FILES}" ] ; then
    content=$content"worker_rlimit_nofile ${NGINX_WORKER_OPEN_FILES};\n"
fi

# Save generated /etc/nginx/nginx.conf
printf "$content" | sed -e 's/\r//g' > /etc/nginx/nginx.conf

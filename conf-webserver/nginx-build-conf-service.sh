#!/usr/bin/env bash
set -e

# Get the listen port for Nginx, default to 80
USE_NGINX_LISTEN_PORT=${NGINX_LISTEN_PORT:-3000}

# Get the service name for the endpoints
USE_SERVICE_NAME=${SERVICE_NAME:-digital_reporter}

content_server='server {\n'
content_server=$content_server"    listen ${USE_NGINX_LISTEN_PORT};\n"
content_server=$content_server"    location /${USE_SERVICE_NAME} {\n"
content_server=$content_server'        include uwsgi_params;\n'
content_server=$content_server"        rewrite /${USE_SERVICE_NAME}/(.*) /\$1 break;\n"
content_server=$content_server'        uwsgi_pass unix:///tmp/uwsgi.sock;\n'
content_server=$content_server'    }\n'
content_server=$content_server'}\n'

# Save generated server /etc/nginx/conf.d/nginx.conf
printf "$content_server" | sed -e 's/\r//g' > /etc/nginx/conf.d/${USE_SERVICE_NAME}.conf

# Generate Nginx config for maximum upload file size
printf "client_max_body_size $USE_NGINX_MAX_UPLOAD;\n" | sed -e 's/\r//g' > /etc/nginx/conf.d/upload.conf


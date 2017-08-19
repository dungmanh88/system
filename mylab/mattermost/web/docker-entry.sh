#!/bin/bash
SERVER_NAME=${SERVER_NAME:-mm.swat.example.com}
NGINX_SITE_CONFIG=/etc/nginx/conf.d/default.conf
#envsubst < /etc/nginx/conf.d/site.template > /etc/nginx/conf.d/default.conf
sed -i '/server_name/s/value/'${SERVER_NAME}'/' ${NGINX_SITE_CONFIG}

echo "Starting nginx server"
exec "$@"

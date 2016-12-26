#!/bin/bash

set -e

export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
pmm_version=pmm-server:1.0.6
pmm_user=
pmm_passwd=

yum -y update && curl -fsSL https://get.docker.com/ | sh &&  systemctl enable docker.service && systemctl start docker

docker create \
   -v /opt/prometheus/data \
   -v /opt/consul-data \
   -v /var/lib/mysql \
   -v /var/lib/grafana \
   --name pmm-data \
   percona/${pmm_version} /bin/true

docker run -d -p 443:443 \
  --volumes-from pmm-data \
  --name pmm-server \
  -e SERVER_USER=${pmm_user} \
  -e SERVER_PASSWORD=${pmm_passwd} \
  -v /etc/pmm-certs:/etc/nginx/ssl \
  --restart always \
  percona/${pmm_version}


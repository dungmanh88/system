#!/bin/bash

common_name=$1

if [ -z $common_name ]; then
  echo "You must enter common_name"
  exit 1
fi

echo "Run file in {{ cert_dir }}"
if [ ! -f domain.key ] || [ ! -f domain.crt ]; then
  openssl req \
    -newkey rsa:4096 -nodes -sha256 -keyout domain.key \
    -x509 -days 365 -out domain.crt -subj "/C=VN/ST=HN/L=Hanoi/O=Global IT/OU=IT Department/CN=${common_name}"
fi
echo "Copy the domain.crt file to /etc/docker/certs.d/${common_name}:5000/ca.crt on every Docker host. You do not need to restart Docker."
echo "Refer: https://docs.docker.com/registry/insecure/#troubleshooting-insecure-registry"

#!/bin/bash

host=$1
port=$2

ssh ${host} -p ${port} mkdir -p /webapp/mattermost

rsync -avzP -e "ssh -p ${port}" docker-compose.yaml ${host}:/webapp/mattermost

# Deploy via ssh
ssh ${host} -p ${port} <<EOF
    set -e
    cd /webapp/mattermost
    docker-compose up
EOF

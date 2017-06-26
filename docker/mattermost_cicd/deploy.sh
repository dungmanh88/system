#!/bin/sh

host=$1
port=$2
dockerComposeVersion=1.14.0

ssh ${host} -p ${port} mkdir -p /webapp/mattermost

rsync -avzP -e "ssh -p ${port}" docker-compose.yaml ${host}:/webapp/mattermost

# Deploy via ssh
ssh ${host} -p ${port} <<EOF
    set -e
    curl -L https://github.com/docker/compose/releases/download/$dockerComposeVersion/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    export PATH=$PATH:/usr/local/bin
    cd /webapp/mattermost
    docker-compose up
EOF

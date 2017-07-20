#!/bin/bash

user=$1
passwd=$2
htpassws_file=$3
docker run \
  --entrypoint htpasswd \
  registry:2 -Bbn ${user} ${passwd} > ${htpassws_file}

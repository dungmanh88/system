#!/bin/bash

set -e 

export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

yum -y install epel-release \
&& yum -y install ansible git gcc gcc-c++ python-devel mariadb-devel openssl-devel wget python-cffi

### support ansible vault
cd /tmp
if [ ! -f /tmp/get-pip.py ]; then
    wget https://bootstrap.pypa.io/get-pip.py 
fi
python get-pip.py \
&& pip install cryptography


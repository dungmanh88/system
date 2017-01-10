#!/bin/bash

set -e 

export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

cd /tmp
if [ ! -f /tmp/get-pip.py ]; then
    wget https://bootstrap.pypa.io/get-pip.py 
fi
### support ansible vault
# then
### generate crypted passwords for the user module
python get-pip.py \
&& pip install cryptography \
&& pip install passlib

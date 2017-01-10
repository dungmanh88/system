#!/bin/bash

set -e 

export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

cd /tmp
if [ ! -f /tmp/get-pip.py ]; then
    wget https://bootstrap.pypa.io/get-pip.py 
fi
python get-pip.py \

### support ansible vault
&& pip install cryptography \

### generate crypted passwords for the user module
&& pip install passlib

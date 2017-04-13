#!/bin/bash

set -e

export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

yum -y install epel-release \
&& yum -y install ansible git gcc gcc-c++ python-devel mariadb-devel openssl-devel wget python-cffi

cat /etc/*release | grep -q "7\."
if [ $? -eq 0 ]; then
  if [ ! -f /tmp/get-pip.py ]; then
      wget -O /tmp/get-pip.py https://bootstrap.pypa.io/get-pip.py
  fi
  ### support ansible vault
  # then
  ### generate crypted passwords for the user module
  python /tmp/get-pip.py \
  && pip install cryptography \
  && pip install passlib
fi

if [ -d /etc/ansible ]; then
  mv /etc/ansible /etc/ansible.bak
fi

# get parent dir of current dir
ln -s "$(dirname "$(pwd)")" /etc/ansible

mkdir -p /etc/.ssh && \
echo -e  'y\n' | ssh-keygen -t rsa -N "" -f /etc/.ssh/ansible_id_rsa

touch /etc/.vault_pass.txt
echo "Your vault passwd: "
read vault_pass
echo "You entered: ${vault_pass}"
echo ${vault_pass} > /etc/.vault_pass.txt

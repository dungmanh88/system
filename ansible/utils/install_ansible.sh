#!/bin/bash

set -e

export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

yum -y install epel-release \
&& yum -y install ansible git gcc gcc-c++ python-devel mariadb-devel openssl-devel wget python-cffi

cat /etc/*release | grep "7\."
if [ $? -eq 0 ]; then
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
fi
cat /etc/*release | grep "6\."
if [ $? -eq 0 ]; then
  echo "chmod u+x install_pip_centos6.sh and run the script"
fi

mkdir -p /etc/.ssh && \
ssh-keygen -t rsa -N "" -f /etc/.ssh/ansible_id_rsa

touch /etc/.vault_pass.txt
echo "Your vault passwd: "
read vault_pass
echo "You entered: ${vault_pass}"
echo ${vault_pass} > /etc/.vault_pass.txt

#!/bin/bash

set -e
export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

version="2.7.9"
url="https://www.python.org/ftp/python/${version}/Python-${version}.tar.xz"
base_dir=/tmp
tar_xz_file=${base_dir}/python.tar.xz
tar_file=${base_dir}/python.tar
install_dir=${base_dir}/Python-${version}

yum groupinstall -y 'development tools' \
&& yum install -y zlib-devel openssl-devel sqlite-devel bzip2-devel \
&& yum install xz-libs

cd ${base_dir}
rm -rf ${tar_xz_file} 
rm -rf ${tar_file}
rm -rf ${install_dir}
wget -O ${tar_xz_file} ${url} \
&& xz -d ${tar_xz_file} \
&& tar -xvf ${tar_file}

cd ${install_dir}
./configure --prefix=/usr/local && make && make altinstall

cd ${base_dir}
if [ ! -f /tmp/get-pip.py ]; then
    wget https://bootstrap.pypa.io/get-pip.py 
fi
### support ansible vault
# then
### generate crypted passwords for the user module
/usr/local/bin/python2.7 get-pip.py \
&& pip install cryptography \
&& pip install passlib

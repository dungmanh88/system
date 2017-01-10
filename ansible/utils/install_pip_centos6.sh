#!/bin/bash

set -e
export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

version="2.7.9"
url="https://www.python.org/ftp/python/${version}/Python-${version}.tar.xz"
tar_xz_file=/tmp/python.tar.xz
tar_file=/tmp/python.tar
install_dir=/tmp/Python-${version}

yum -y update \
&& yum groupinstall -y 'development tools' \
&& yum install -y zlib-devel openssl-devel sqlite-devel bzip2-devel \
&& yum install xz-libs

wget -O ${tar_xz_file} ${url} \
&& xz -d ${tar_xz_file} \
&& tar -xvf ${tar_file}

cd ${install_dir}
./configure --prefix=/usr/local  && make && make altinstall

export PATH="/usr/local/bin:$PATH"
pip install -U pip setuptools virtualenv

pip install cryptography
pip install passlib

#!/bin/bash
yum -y install epel-release
cd /tmp
wget https://rpms.remirepo.net/enterprise/remi-release-7.rpm
rpm -vih remi-release-7.rpm
yum -y install --enablerepo=remi-php71,remi php php-fpm php-mysql php-mbstring php-xml
yum -y install nginx mysql
systemctl start nginx
systemctl start php-fpm
systemctl enable nginx
systemctl enable php-fpm

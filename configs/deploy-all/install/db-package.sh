#!/bin/bash
yum -y install epel-release
yum -y install mysql mariadb-server
systemctl start mariadb
systemctl enable mariadb

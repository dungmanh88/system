#http://yum.opensips.org/howto.php

#yum -y install http://yum.opensips.org/2.3/releases/el/7/x86_64/opensips-yum-releases-2.3-3.el7.noarch.rpm
#yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
#yum -y install opensips
#systemctl start opensips
#systemctl enable opensips
#Bản opensips này không hỗ trợ db

wget http://opensips.org/pub/opensips/latest/opensips-2.3.2.tar.gz
cd opensips-2.3.2
https://github.com/OpenSIPS/opensips/blob/master/INSTALL
https://www.opensips.org/Documentation/Install-CompileAndInstall-2-3
yum -y install gcc gcc-c++ make bison flex openssl-devel libxml2-devel ncurses-devel
make clean
make all

yum -y install mariadb-server
systemctl start mariadb-server
systemctl enable mariadb-server

/etc/opensips/opensipsctlrc
```
DBENGINE=MYSQL
DBPORT=3306
DBHOST=localhost
DBNAME=opensips
DBRWUSER=opensips
DBRWPW="opensipsrw"
DBROOTUSER="root"
ETCDIR="/etc/opensips"
```

MariaDB [(none)]> create database opensips;
Query OK, 1 row affected (0.00 sec)

MariaDB [(none)]> grant all privileges on `opensips`.* to 'opensips'@'localhost' identified by 'opensipsrw';
Query OK, 0 rows affected (0.00 sec)

make menuconfig > configure compile options
-> customize install path > configure install prefix, default /usr/local
-> customize module > configure excluded module -> db_mysql
q > save > re-compile and re-install opensips make all && make install

make install

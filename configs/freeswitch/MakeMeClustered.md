Use mod_xml_curl to pull xml from web page
This will seperate data, config from Freeswitch. It help make it clustered

http://saevolgo.blogspot.com/2012/07/freeswitch-with-sip-users-in-mysql-mod.html
Freeswitch 1.2 ebook

**You must install FS from source to enable mod_xml_curl**
https://freeswitch.org/confluence/display/FREESWITCH/mod_xml_curl#mod_xml_curl-Installation
cd /usr/local/src/freeswitch
vi modules.conf
Uncomment this line
xml_int/mod_xml_curl

recompile and install
```
make mod_xml_curl && make mod_xml_curl-install
```

/etc/freeswitch/autoload_configs/modules.conf.xml
Load module auto
```
<!-- Loggers (I'd load these first) -->
<load module="mod_console"/>
<!-- <load module="mod_graylog2"/> -->
<load module="mod_logfile"/>
<load module="mod_xml_curl"/> ### put on the top of modules.conf.xml
```

mv /etc/freeswitch/autoload_configs/xml_curl.conf.xml /etc/freeswitch/autoload_configs/xml_curl.conf.xml.bak
/etc/freeswitch/autoload_configs/xml_curl.conf.xml
```
<configuration name="xml_curl.conf" description="curlconf">
  <bindings>
    <binding name="freeswitch_backend">
       <param name="gateway-url" value="http://localhost/fs_curl/index.php" bindings="directory"/>
    </binding>
  </bindings>
</configuration>
```

systemctl restart freeswitch
fs_cli -x "show module" to check

yum -y install mysql mariadb-server php-pdo curl php-xml php php-mysql php-pear php-gd php-pear php-pdo

cd /etc/php.d
[root@template-centos7 default]# vi /etc/php.d/pdo_mysql.ini
extension=pdo_mysql.so
[root@template-centos7 default]# vi /etc/php.d/mysql.ini
extension=mysql.so
[root@template-centos7 default]# vi /etc/php.d/pdo.ini
extension=pdo.so

systemctl start mariadb && \
systemctl enable mariadb
yum -y install httpd
systemctl start httpd
vi /etc/httpd/conf.d/php.conf
enable php for httpd

Load module php into /etc/httpd/conf.modules.d/10-php.conf
```
<IfModule prefork.c>
  LoadModule php5_module modules/libphp5.so
</IfModule>
```
systemctl restart httpd

cd /tmp
https://freeswitch.org/stash/projects/FS/repos/freeswitch-contrib/browse/intralanman/PHP/fs_curl
git clone https://freeswitch.org/stash/scm/fs/freeswitch-contrib.git
mkdir /var/www/html/fs_curl
cd freeswitch-contrib/intralanman/PHP/fs_curl/
cp -rf * /var/www/html/fs_curl
cd /var/www/html/fs_curl/
global_defines.php
```
define('DEFAULT_DSN', 'mysql:dbname=freeswitch;host=127.0.0.1');
define('DEFAULT_DSN_LOGIN', 'freeswitch');
define('DEFAULT_DSN_PASSWORD', 'Fr33Sw1tch');

If you want to debug uncomment the following (Not recommended for production servers)


define('FS_CURL_DEBUG', 9); // uncomment
define('FS_DEBUG_TYPE', 2); // 0-> 2
define('FS_DEBUG_FILE', '/var/log/fs_curl.debug');
```

touch /var/log/fs_curl.debug
chown -R apache:apache /var/log/fs_curl.debug

fs_directory.php
```
#In get_directory function
#change
#$where_array[]   = sprintf( "domain_id='%s'", $domain['id'] );
#to
Keep
$where_array[]   = sprintf( "domain_id='%s'", $domain ['id'] );

change
$query = sprintf( "SELECT * FROM directory d %s %s ORDER BY username", $join_clause, $where_clause );
to
$query = sprintf( "SELECT * FROM directory %s %s ORDER BY username", $join_clause, $where_clause );
```

mysql>
create database freeswitch;
grant all privileges on `freeswitch`.* to 'freeswitch'@'127.0.0.1' identified by 'Fr33Sw1tch';

cd /var/www/html/fs_curl/sql
mysql -u root -p freeswitch < mysql-5.0-with-samples.sql

use freeswitch

mysql> insert into directory_domains values (3,'lb-ip');
Query OK, 1 row affected (0.00 sec)

MariaDB [freeswitch]> select * from directory_domains;
+----+----------------+
| id | domain_name    |
+----+----------------+
|  1 | freeswitch.org |
|  2 | sofaswitch.org |
|  3 | lb-ip|
+----+----------------+


mysql>INSERT into directory (username,domain_id) VALUES ("40277",3);
mysql>INSERT into directory (username,domain_id) VALUES ("50354",3);


GET THE "id" from the directory table for these newly created users.
MariaDB [freeswitch]> select * from directory;
+----+----------+-----------+-------+
| id | username | domain_id | cache |
+----+----------+-----------+-------+
|  1 | 1000     |         1 |     0 |
|  2 | 1001     |         2 |     0 |
|  3 | 1002     |         1 |     0 |
|  5 | 1003     |         2 |     0 |
|  6 | 1004     |         1 |     0 |
|  7 | 1005     |         2 |     0 |
|  8 | 1006     |         1 |     0 |
|  9 | 1007     |         2 |     0 |
| 10 | 2000     |         1 |     0 |
| 11 | 1009     |         2 |     0 |
| 12 | 40277    |         3 |     0 |
| 13 | 50354    |         3 |     0 |
+----+----------+-----------+-------+


```
mysql> insert into directory_params (directory_id,param_name,param_value) VALUES (12,'password','40277');
mysql> insert into directory_params (directory_id,param_name,param_value) VALUES (13,'password','50354');


mysql> insert into directory_vars(directory_id, var_name, var_value) VALUES (12, 'user_context', 'default');
mysql> insert into directory_vars(directory_id, var_name, var_value) VALUES (13, 'user_context', 'default');

mysql> insert into directory_global_params(param_name, param_value, domain_id) VALUES ("dial-string", "{^^:sip_invite_domain=${dialed_domain}:presence_id=${dialed_user}@${dialed_domain}}${sofia_contact(*/${dialed_user}@${dialed_domain})},${verto_contact(${dialed_user}@${dialed_domain})}", 3);
```


Modify something
/etc/freeswitch/dialplan/default.xml
```
<extension name="Local_Extension">
  <condition field="destination_number" expression="^(10[01][0-9]|50354|40227)$">
```

Thats All, now try registering your SOFT Phone using new username/password and see if your requests reach to WEB-Server.
You can troubleshoot the XML_CURL module by issuing the following command on FS Console.
fs_cli
freeswitch@internal> xml_curl debug_on
OK

**Repeat with other FS with one DB**

By default, you get
```
<document type="freeswitch/xml">
<section name="result">
<result status="not found"/>
</section>
<!--
 ERROR: 8 - (Undefined index: section) on line 61 of /var/www/html/fs_curl/index.php
-->
</document>
```
when curl http://localhost/fs_curl/index.php


https://github.com/intralanman/fs_curl

[root@template-centos7 directory]# cp -r /etc/freeswitch/directory/default /etc/freeswitch/directory/default.bak
[root@template-centos7 directory]# cd /etc/freeswitch/directory/default
[root@template-centos7 default]# rm -rf *

restart all service: fs, httpd, mariadb

Test 40277 and 50354 with domain lb-ip (you will use LB)
If you don't use LB, you will get domain of FS not LB, and register to FS directly

http://fs-ip/fs_curl/index.php?section=directory&user=40277&domain=fs-ip
you will see info

If you change db, you must restart fs to reload xml

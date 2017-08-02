# Install
```
yum -y install epel-release \
mysql mariadb-server
systemctl start mariadb
systemctl enable mariadb

yum -y install nginx php php-fpm php-mysql php-mbstring php-imap
systemctl start nginx && \
systemctl enable nginx && \
systemctl start php-fpm && \
systemctl enable php-fpm

tar xvzf postfixadmin-3.1.tar.gz
mv postfixadmin-3.1 postfixadmin
```

# Config database
```
CREATE DATABASE postfix;
 CREATE USER 'postfix'@'localhost' IDENTIFIED BY 'postfix';
 GRANT ALL PRIVILEGES ON `postfix` . * TO 'postfix'@'localhost';
```

# Config postfixadmin

postfixadmin/config.local.php
```
<?php
$CONF['database_type'] = 'mysqli';
$CONF['database_user'] = 'postfix';
$CONF['database_password'] = 'postfix';
$CONF['database_name'] = 'postfix';

$CONF['configured'] = true;

$CONF['domain_path'] = 'YES';
$CONF['domain_in_mailbox'] = 'NO';
?>
```

# Create templates_c in postfixadmin
```
cd postfixadmin
mkdir -p templates_c
chmod o+rwx templates_c/
```

# Config web
/etc/nginx/conf.d/postfixadmin.conf
```
/etc/nginx/conf.d/vhost.conf
server {

  index index.php index.html;
  server_name postfixadmin.lab.com www.postfixadmin.lab.com;
  error_log /var/log/nginx/postfixadmin.lab.com/error.log;
  client_max_body_size 20M;
  access_log /var/log/nginx/postfixadmin.lab.com/access.log;
  root /data/www/html/postfixadmin;
  listen 80;

  location / {
  }

  location ~ \.php$ {
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    include /etc/nginx/fastcgi_params;
    fastcgi_index index.php;
    fastcgi_pass 127.0.0.1:9000;
  }
}
```
mkdir -p /var/log/nginx/postfixadmin.lab.com
mkdir -p /data/www/html/postfixadmin

systemctl restart nginx
systemctl restart php-fpm

# Create admin user
```
http://postfixadmin.lab.com/setup.php
admin/genpass
```
NOTICE:
```
If you want to use the password you entered as setup password, edit config.inc.php or config.local.php and set
$CONF['setup_password'] = '28603e3cac94fa19c59d38b7adfa3b1f:5381c6fb4346f97c7abeac605b45ccac4d4b6962';
```
Add
```
$CONF['setup_password'] = '28603e3cac94fa19c59d38b7adfa3b1f:5381c6fb4346f97c7abeac605b45ccac4d4b6962';
```
into postfixadmin/config.local.php

email admin must be a real email in domain lab.com

# Test admin account
```
http://postfixadmin.lab.com/login.php
```
adam@lab.com + admin password (not setup password)

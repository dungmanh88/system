https://www.rosehosting.com/blog/setup-and-configure-a-mail-server-with-postfixadmin/
https://github.com/postfixadmin/postfixadmin/tree/master/DOCUMENTS
https://wiki.archlinux.org/index.php/Virtual_user_mail_system#Dovecot
https://wiki.dovecot.org/BasicConfiguration
https://www.howtoforge.com/community/threads/proper-postfix-and-dovecot-configuration-after-installing-ispconfig.63289/
https://serverfault.com/questions/334850/dovecot-auth-fatal-unknown-database-driver-pgsql


Inherit from send-receive-mail-LAN, customize from send-receive-mail-LAN/GUIDE.md

# Install
```
yum -y install epel-release \
mysql mariadb-server
systemctl start mariadb && \
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

$CONF['used_quotas'] = 'YES';
$CONF['quota'] = 'YES';
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
mkdir -p /var/log/nginx/postfixadmin.lab.com && \
mkdir -p /data/www/html/postfixadmin

systemctl restart nginx && \
systemctl restart php-fpm

# Create admin user
```
http://postfixadmin.lab.com/setup.php
Create setup password
```
NOTICE:
```
If you want to use the password you entered as setup password, edit config.inc.php or config.local.php and set
$CONF['setup_password'] = 'xyz...';
```
Add
```
$CONF['setup_password'] = 'xyz...';
```
into postfixadmin/config.local.php

email admin must be a email in domain lab.com
admin (such as admin@lab.com) - this account is a isolated account for postfixadmin management (not email account)

# Test admin account
```
http://postfixadmin.lab.com/login.php
```
admin@lab.com + password (not setup password)

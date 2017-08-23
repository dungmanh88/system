```
Put source code into web1_ws and web2_ws
vagrant ssh web1
vagrant ssh web2
vagrant ssh db
vagarnt ssh proxy
```
App
.env
```
DB_CONNECTION=mysql
DB_HOST=192.168.56.103
DB_PORT=3306
DB_DATABASE=nissan
DB_USERNAME=nissan
DB_PASSWORD=nissan
```
cp -r nissan_user_portal/* web1_ws/
cp -r nissan_user_portal/* web2_ws/

PROXY: 192.168.56.100 - cache
yum -y install epel-release
yum -y install nginx httpd-tools
systemctl start nginx
systemctl enable nginx

/etc/nginx/conf.d/web.conf
```
upstream myapp {
    server 192.168.56.101:80;
    server 192.168.56.102:80;
}

server {

  server_name workshop.lab.local;
  error_log /var/log/nginx/workshop.lab.local/error.log;
  access_log /var/log/nginx/workshop.lab.local/access.log;
  listen 80;
  location / {
    proxy_pass http://myapp;
    proxy_set_header HOST $host;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_cache workshop_cache;
    #  If the header includes the "Set-Cookie" field, such a response will not be cached.
    proxy_ignore_headers Set-Cookie;
    proxy_cache_use_stale error timeout updating http_500 http_502
                          http_503 http_504;
    proxy_cache_lock on;
    proxy_cache_valid 200 302 10m;
    proxy_cache_valid 404      1m;
  }
}

proxy_cache_path /cache/nginx/workshop levels=1:2 keys_zone=workshop_cache:10m max_size=1g inactive=60m use_temp_path=off;
```
mkdir -p /var/log/nginx/workshop.lab.local
mkdir -p /cache/nginx/workshop

WEB1: 192.168.56.101 - web
yum -y install epel-release
yum -y install nginx httpd-tools php-fpm php php-mysql
systemctl start nginx
systemctl start php-fpm
systemctl enable nginx
systemctl enable php-fpm

/etc/nginx/conf.d/web.conf
```
server {

  index index.php index.html;
  server_name workshop.lab.local;
  error_log /var/log/nginx/workshop.lab.local/error.log;
  client_max_body_size 20M;
  access_log /var/log/nginx/workshop.lab.local/access.log;
  root /srv/website/public;
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
mkdir -p /var/log/nginx/workshop.lab.local
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
php composer-setup.php
php -r "unlink('composer-setup.php');"
php composer.phar install

php artisan key:generate

php artisan config:cache

php artisan cache:clear

php artisan optimize

php artisan migrate


WEB2: 192.168.56.102 - web
yum -y install epel-release
yum -y install nginx httpd-tools php-fpm php php-mysql
systemctl start nginx
systemctl start php-fpm
systemctl enable nginx
systemctl enable php-fpm

/etc/nginx/conf.d/web.conf
```
server {

  index index.php index.html;
  server_name workshop.lab.local;
  error_log /var/log/nginx/workshop.lab.local/error.log;
  client_max_body_size 20M;
  access_log /var/log/nginx/workshop.lab.local/access.log;
  root /srv/website/public;
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
mkdir -p /var/log/nginx/workshop.lab.local
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
php composer-setup.php
php -r "unlink('composer-setup.php');"
php composer.phar install

php artisan key:generate

php artisan config:cache

php artisan cache:clear

php artisan optimize

php artisan migrate

DB: 192.168.56.103 - db
yum -y install epel-release
yum -y install mysql mariadb-server
systemctl start mariadb
systemctl enable mariadb
mysql_secure_installation root/abc123
mysql -u root -p
create database nissan;
grant all privileges on `nissan`.* to 'nissan'@'192.168.56.0/24' identified by 'nissan';

config 127.0.0.1 workshop.lab.local

http://workshop.lab.local:8080

vagrant halt proxy
vagrant halt db
vagrant halt web1
vagrant halt web2

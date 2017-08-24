```
vagrant up
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
Put source code into web1_ws and web2_ws
cp -r nissan_user_portal/* web1_ws/
cp -r nissan_user_portal/* web2_ws/
cp nissan_user_portal/.env web1_ws/
cp nissan_user_portal/.env web2_ws/
cd web1,2_ws/public
rm -rf storage/
ln -s ../storage/app/public/ storage

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
    index index.html index.php;
    proxy_pass http://myapp;
    proxy_set_header  Host $http_host;
    proxy_set_header  X-Real-IP $remote_addr;
    proxy_set_header  X-Forwarded-Proto http;
    proxy_set_header  X-Forwarded-For $remote_addr;
    proxy_set_header  X-Forwarded-Host $remote_addr;

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

proxy_cache_path /cache/nginx/workshop levels=1:2 keys_zone=workshop_cache:10m max_size=20m inactive=60m use_temp_path=off;
```
mkdir -p /var/log/nginx/workshop.lab.local
mkdir -p /cache/nginx/workshop
chown -R nginx:nginx /var/log/nginx/workshop.lab.local
chown -R nginx:nginx /cache/


WEB1: 192.168.56.101 - web
yum -y install epel-release
cd /tmp
wget https://rpms.remirepo.net/enterprise/remi-release-7.rpm
rpm -vih remi-release-7.rpm
yum -y install --enablerepo=remi-php71,remi php php-fpm php-mysql php-mbstring php-xml
yum -y install nginx httpd-tools mysql
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
       index index.html index.php;
       try_files $uri $uri/ /index.php?$query_string;
  }

  location ~ \.php$ {
    fastcgi_pass 127.0.0.1:9000;
    fastcgi_index index.php;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    include /etc/nginx/fastcgi_params;
  }
}
```
useradd -d /dev/null -c "www-data user" -s /sbin/nologin www-data
usermod -a -G www-data nginx
id nginx
usermod -a -G www-data apache
id apache

mkdir -p /var/log/nginx/workshop.lab.local
mkdir -p /srv/website
cp -r /data/* /srv/website
cp /data/.env /srv/website

chown -R www-data:www-data /srv/website
find /srv/website -type f -exec chmod 664 {} \;
find /srv/website -type d -exec chmod 775 {} \;

cd /srv/website
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
php composer-setup.php
php -r "unlink('composer-setup.php');"
php composer.phar install

php artisan key:generate && \

php artisan config:cache && \

php artisan cache:clear && \

php artisan optimize && \

php artisan migrate


WEB2: 192.168.56.102 - web
yum -y install epel-release
cd /tmp
wget https://rpms.remirepo.net/enterprise/remi-release-7.rpm
rpm -vih remi-release-7.rpm
yum -y install --enablerepo=remi-php71,remi php php-fpm php-mysql php-mbstring php-xml
yum -y install nginx httpd-tools mysql
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
       index index.html index.php;
       try_files $uri $uri/ /index.php?$query_string;
  }

  location ~ \.php$ {
    fastcgi_pass 127.0.0.1:9000;
    fastcgi_index index.php;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    include /etc/nginx/fastcgi_params;
  }
}
```
useradd -d /dev/null -c "www-data user" -s /sbin/nologin www-data
usermod -a -G www-data nginx
usermod -a -G www-data apache

mkdir -p /var/log/nginx/workshop.lab.local
mkdir -p /srv/website
cp -r /data/* /srv/website
cp /data/.env /srv/website

chown -R www-data:www-data /srv/website
find /srv/website -type f -exec chmod 664 {} \;
find /srv/website -type d -exec chmod 775 {} \;

cd /srv/website
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
php composer-setup.php
php -r "unlink('composer-setup.php');"
php composer.phar install

php artisan key:generate && \

php artisan config:cache && \

php artisan cache:clear && \

php artisan optimize && \

php artisan migrate

DB: 192.168.56.103 - db
yum -y install epel-release
yum -y install mysql mariadb-server
systemctl start mariadb
systemctl enable mariadb
mysql_secure_installation root/abc123
mysql -u root -p
create database nissan;
grant all privileges on `nissan`.* to 'nissan'@'192.168.56.%' identified by 'nissan';

config 127.0.0.1 workshop.lab.local

restart all service nginx, php-fpm, mariadb
http://workshop.lab.local:8080
siege -c 10000 -t10s -d 5 http://workshop.lab.local:8080/login


vagrant halt
